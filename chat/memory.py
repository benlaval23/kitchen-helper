def read_stock_file():
    file_path = "./files/memory/stock_list.txt"
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

def overwrite_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while writing to file '{file_path}': {e}")
        return None