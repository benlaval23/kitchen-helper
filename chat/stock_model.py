
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

os.getenv("OPENAI_API_KEY")

stock_model = ChatOpenAI(model_name="gpt-4o")

stock_prompt = PromptTemplate(
    input_variables=["current_time", "stock_list", "suggested_update"],
    template="""Your are an kitchen stock manager, using the current stock list and the suggested changes, return the updated stock list ONLY. Next to each item, add the time the item was added.
                Current Time: {current_time} 
                Current Stock: {stock_list}
                Suggested Update: {suggested_update}
                Updated Stock List: """
    )

stock_chain = stock_prompt | stock_model