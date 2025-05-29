import glob
import os

from src.utils.consts import CBOR_FILE_EXT, JADN_SCHEMA_FILE_EXT, JSON_FILE_EXT, UNKNOWN_EXT, XML_FILE_EXT, XSD_FILE_EXT
    
def get_file(dir_path: str, filename: str) -> dict:
    file_data = {}
    filepath = os.path.join(dir_path, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            file_data[filename] = file.read()
            
    return file_data

def determine_file_type(filename: str) -> str:
    """
    Determine the file type based on the file extension.
    Returns 'jadn' for JADN schema files, 'json' for JSON files, or 'unknown' for others.
    """
    if filename.endswith('.cbor'):
        return CBOR_FILE_EXT    
    elif filename.endswith('.jadn'):
        return JADN_SCHEMA_FILE_EXT
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

def list_files(dir):
    """
    List all files in the specified directory.
    """
    dir = os.path.join(os.getcwd(), dir)
    if not os.path.exists(dir):
        print(f"The '{dir}' directory does not exist.")
        return
    
    files = glob.glob(os.path.join(dir, "*"))
    if files:
        print(f"Files in '{dir}' directory:")
        for f in files:
            print("  -", os.path.basename(f))
    else:
        print(f"No files found in the '{dir}' directory.")
        
def pick_a_file(dir, prompt="Enter the filename (or type 'exit' to cancel): ") -> str:
    """
    Prompt the user to pick a file from the specified directory.
    Returns the selected filename or None if cancelled.
    """
    dir = os.path.join(os.getcwd(), dir)
    if not os.path.exists(dir):
        print(f"The '{dir}' directory does not exist.")
        return None
    
    files = [os.path.basename(f) for f in glob.glob(os.path.join(dir, "*"))]
    
    if not files:
        print(f"No files found in the '{dir}' directory.")
        return None
    
    while True:
        filename = input(prompt).strip()
        if filename.lower() == 'exit':
            print("Operation cancelled.")
            return None
        if filename in files:
            return filename
        else:
            print("Invalid filename. Please try again or type 'exit' to cancel.")        