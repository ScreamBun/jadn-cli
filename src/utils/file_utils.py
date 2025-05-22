import os
    
def get_file(dir_path: str, filename: str) -> dict:
    file_data = {}
    filepath = os.path.join(dir_path, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            file_data[filename] = file.read()
            
    return file_data    