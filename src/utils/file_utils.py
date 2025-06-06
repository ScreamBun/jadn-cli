import glob
import json
import os

from src.utils.consts import CBOR_FILE_EXT, JADN_SCHEMA_FILE_EXT, JIDL_FILE_EXT, JSON_FILE_EXT, UNKNOWN_EXT, XML_FILE_EXT, XSD_FILE_EXT
    
def get_file(dir_path: str, filename: str) -> dict:
    file_data = {}
    filepath = os.path.join(dir_path, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            file_data[filename] = file.read()
            
    return file_data

def get_filepath(dir_path: str, filename: str) -> str:
    """
    Returns the absolute full path to the file if it exists, otherwise returns None.
    """
    filepath = os.path.join(dir_path, filename)
    if os.path.isfile(filepath):
        return os.path.abspath(filepath)
    return None

def determine_file_type(filename: str) -> str:
    """
    Determine the file type based on the file extension.
    Returns 'jadn' for JADN schema files, 'json' for JSON files, or 'unknown' for others.
    """
    if filename.endswith('.cbor'):
        return CBOR_FILE_EXT    
    elif filename.endswith('.jadn'):
        return JADN_SCHEMA_FILE_EXT
    elif filename.endswith('.jidl'):
        return JIDL_FILE_EXT    
    elif filename.endswith('.json'):
        return JSON_FILE_EXT
    elif filename.endswith('.xml'):
        return XML_FILE_EXT
    elif filename.endswith('.xsd'):
        return XSD_FILE_EXT        
    else:
        return UNKNOWN_EXT

def file_exists(dirname, filename):
    """
    Check if a filename exists in the directory.
    Returns True if found, False otherwise.
    """
    dir = os.path.join(os.getcwd(), dirname)
    if not os.path.exists(dir):
        return False
    files = [os.path.basename(f) for f in glob.glob(os.path.join(dir, "*"))]
    return filename in files

def list_files(dir, is_jadn_only=True):
    """
    List all files (not directories or nested files) in the specified directory, displaying a file number for each.
    """
    dir = os.path.join(os.getcwd(), dir)
    if not os.path.exists(dir):
        print(f"The '{dir}' directory does not exist.")
        return

    if is_jadn_only:
        files = [f for f in glob.glob(os.path.join(dir, "*.jadn")) if os.path.isfile(f)]
    else:
        files = [f for f in glob.glob(os.path.join(dir, "*")) if os.path.isfile(f)]
        
    if files:
        print(f"Files in '{dir}' directory:")
        for idx, f in enumerate(files, 1):
            print(f"  {idx} - {os.path.basename(f)}")
    else:
        print(f"No files found in the '{dir}' directory.")

# def list_files(dir, file_ext=None):
    # """
    # List all files (not directories or nested files) in the specified directory, displaying a file number for each.
    # If file_ext is provided (e.g., '.jadn'), only files with that extension are shown.
    # """
    # dir = os.path.join(os.getcwd(), dir)
    # if not os.path.exists(dir):
    #     print(f"The '{dir}' directory does not exist.")
    #     return

    # if file_ext:
    #     if not file_ext.startswith('.'):
    #         file_ext = '.' + file_ext
    #     files = [f for f in glob.glob(os.path.join(dir, f"*{file_ext}")) if os.path.isfile(f)]
    # else:
    #     files = [f for f in glob.glob(os.path.join(dir, "*")) if os.path.isfile(f)]

    # if files:
    #     print(f"Choose a file:")
    #     for idx, f in enumerate(files, 1):
    #         print(f"  {idx} - {os.path.basename(f)}")
    # else:
    #     print(f"No files found in the '{dir}' directory{f' with extension {file_ext}' if file_ext else ''}.")
        
def pick_an_option(opts, opts_title="Choose an option:", prompt="Enter an option number or name (or type 'exit' to cancel): ") -> str:
    """
    Prompt the user to pick an option by index or name.
    Returns the selected option (by name) or None if cancelled.
    """
    print(f"{opts_title}")
    for idx, opt in enumerate(opts, 1):
        print(f"  {idx} - {opt}")    
    
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'exit':
            print("Operation cancelled.")
            return None
        # Check if input is a valid index
        if user_input.isdigit():
            index = int(user_input)
            if 1 <= index <= len(opts):
                return opts[index - 1]
        # Check if input matches an option name
        if user_input in opts:
            return user_input
        print("Invalid option entered. Please try again or type 'exit' to cancel.")    

def pick_a_file(dir, is_jadn_only=True, prompt="Enter the file number or filename (or type 'exit' to cancel): ") -> str:
    """
    Prompt the user to pick a file from the specified directory.
    Returns the selected filename or None if cancelled.
    Only files at the dir level (no directories or nested files) are shown.
    """
    dir = os.path.join(os.getcwd(), dir)
    if not os.path.exists(dir):
        print(f"The '{dir}' directory does not exist.")
        return None

    if is_jadn_only:
        files = [os.path.basename(f) for f in glob.glob(os.path.join(dir, "*.jadn")) if os.path.isfile(f)]
    else:
        files = [os.path.basename(f) for f in glob.glob(os.path.join(dir, "*")) if os.path.isfile(f)]

    if not files:
        print(f"No files found in the '{dir}' directory.")
        return None

    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'exit':
            print("Operation cancelled.")
            return None
        # Allow picking by index
        if user_input.isdigit():
            index = int(user_input)
            if 1 <= index <= len(files):
                return files[index - 1]
        # Allow picking by filename
        if user_input in files:
            return user_input
        
        print("Invalid selection. Please enter a valid number, filename, or 'exit' to cancel.")

# def pick_a_file(dir, file_ext=None, prompt="Enter the file number or filename (or type 'exit' to cancel): ") -> str:
#     """
#     Prompt the user to pick a file from the specified directory.
#     Returns the selected filename or None if cancelled.
#     Only files at the dir level (no directories or nested files) are shown.
#     If file_ext is provided (e.g., '.jadn'), only files with that extension are shown.
#     """
#     dir = os.path.join(os.getcwd(), dir)
#     if not os.path.exists(dir):
#         print(f"The '{dir}' directory does not exist.")
#         return None

#     if file_ext:
#         if not file_ext.startswith('.'):
#             file_ext = '.' + file_ext
#         files = [os.path.basename(f) for f in glob.glob(os.path.join(dir, f"*{file_ext}")) if os.path.isfile(f)]
#     else:
#         files = [os.path.basename(f) for f in glob.glob(os.path.join(dir, "*")) if os.path.isfile(f)]

#     if not files:
#         print(f"No files found in the '{dir}' directory{f' with extension {file_ext}' if file_ext else ''}.")
#         return None

#     print(f"Files in '{dir}' directory{f' with extension {file_ext}' if file_ext else ''}:")
#     for idx, f in enumerate(files, 1):
#         print(f"  {idx} - {f}")

#     while True:
#         user_input = input(prompt).strip()
#         if user_input.lower() == 'exit':
#             print("Operation cancelled.")
#             return None
#         # Allow picking by index
#         if user_input.isdigit():
#             index = int(user_input)
#             if 1 <= index <= len(files):
#                 return files[index - 1]
#         # Allow picking by filename
#         if user_input in files:
#             return user_input
        
#         print("Invalid selection. Please enter a valid number, filename, or 'exit' to cancel.")
                          
def update_file_extension(filename, new_ext):
    """
    Update a filename with a new extension.
    Returns the new filename.
    Example: update_file_extension('example.txt', '.json') -> 'example.json'
    """
    base = os.path.splitext(filename)[0]
    if not new_ext.startswith('.'):
        new_ext = '.' + new_ext
    return base + new_ext            
            
def write_to_output(filename, data):
    """
    Write data to a file under the 'output' directory.
    Creates the directory if it does not exist.
    """
    
    if not isinstance(data, str):
        data = str(data)  # Ensure data is a string
    
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        f.write(data)
    print(f" - Data written to {filepath}/{filename}")
    
def write_json_to_output(filename, data):
    """
    Write json data to a file under the 'output' directory.
    Creates the directory if it does not exist.
    """
    
    if not isinstance(data, str):
        data = json.dumps(data, indent=4)        # Ensure data is a string
    
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        f.write(data)
    print(f" - Data written to {filepath}/{filename}")    