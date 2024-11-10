from chat.memory import read_stock_file
from chat.stock_model import stock_chain
from chat.memory import overwrite_file
import time 

## Schema for the function
functions = [
    {
        "name": "update_stock_list",
        "description": "Update the kitchen stock list, either when new items are bought/added, or current items are eaten/removed. Only run this function, when prompted to update stock list.",
        "parameters": {
            "type": "object",
            "properties": {
                "suggested_changes": {
                    "type": "string",
                    "description": "The requestted changes to the stock list.",
                },
                "edit_type": {
                    "type": "string",
                    "description": "Whether to add or remove the item.",
                    "enum": ["add", "remove", "update"]
                }
            },
            "required": ["suggested_changes", "edit_type"], 
        }
    }
]

## Functions
def update_stock_list(suggested_changes, edit_type):
    stock_list = read_stock_file()
    print(f"Current stock: {stock_list}")
    print(f"Suggested changes: {suggested_changes}")
    current_time = time.strftime("%Y-%m-%d")
    response = stock_chain.invoke({"current_time": current_time, "stock_list": stock_list, "suggested_update": f'{edit_type}: {suggested_changes}'})
    print(response.content)
    overwrite_file("./files/memory/stock_list.txt", response.content)
    return response.content
    

## Function lookup
function_calls = {
    "update_stock_list": update_stock_list
}