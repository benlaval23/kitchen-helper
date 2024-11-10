
from chat.functions import functions
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model_name="gpt-4o", streaming=True, model_kwargs={"functions": functions})

prompt = PromptTemplate(
    input_variables=["question", "stock_list", "chat_history"],
    template="""Your are a kitchen assistant, designed to give recipe suggestions based on the stock. IF ASKED SPECIFICALLY, you can also update the stock list, this SHOULD ONLY be done if the user has added or removed items physically and asked you to update the stock list to match. 
                Chat History: {chat_history} 
                Stock: {stock_list}
                Question: {question}"""
    )

chain = prompt | model