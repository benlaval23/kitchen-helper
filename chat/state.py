import reflex as rx
from chat.memory import read_stock_file
from chat.model import chain
from chat.functions import function_calls
import json

class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str

DEFAULT_CHATS = {
    "Recipes": [],
}

class State(rx.State):
    """The app state."""

    # Dictionary to store chats and questions
    chats: dict[str, list[QA]] = DEFAULT_CHATS
    current_chat = "Recipes"
    question: str
    processing: bool = False
    new_chat_name: str = ""

    def create_chat(self):
        """Create a new chat."""
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]

    def set_chat(self, chat_name: str):
        """Set the name of the current chat."""
        self.current_chat = chat_name

    @rx.var
    def chat_titles(self) -> list[str]:
        """Return chat titles."""
        return list(self.chats.keys())

    async def process_question(self, form_data: dict[str, str]):
        # Retrieve and validate question input
        question = form_data.get("question", "").strip()
        if not question:
            return

        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)
        self.processing = True
        yield  # Start processing

        # Process question asynchronously using LangChain
        async for answer in self.langchain_answer(question):
            qa.answer += answer
            self.chats = self.chats
            yield

        self.processing = False

    async def langchain_answer(self, question: str):
        """Use LangChain to get answers from the model."""
        chat_history = "\n".join(f"Q: {qa.question}\nA: {qa.answer}" for qa in self.chats[self.current_chat])
        
        stock_list = read_stock_file()
        
        args = ''
        function_name = ''
        function_required = False
        
        # Use a synchronous loop and yield each response asynchronously
        for response in chain.stream({"question": question, "chat_history": chat_history, "stock_list": stock_list}):
            print(response)
            if 'function_call' in response.additional_kwargs:
                function_required = True
                                    
                function_call = response.additional_kwargs['function_call']
                response_args = function_call['arguments']
                args += response_args
                if function_name == '':
                    function_name = function_call['name']
                
            if 'finish_reason' in response.response_metadata and function_required == True:
                print(f'Running {function_name} with {args}')
                
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        raise ValueError("Unable to parse args as JSON.")
                
                if function_name in function_calls:
                    function = function_calls[function_name]
                    result = function(args['suggested_changes'], args['edit_type'])  # Call the function with the provided arguments
                    
                    yield result  # Return the function's result as part of the response
            

            else:
                yield response.content