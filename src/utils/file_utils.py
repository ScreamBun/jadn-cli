import glob
import os
    
def get_file(dir_path: str, filename: str) -> dict:
    file_data = {}
    filepath = os.path.join(dir_path, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            file_data[filename] = file.read()
            
    return file_data

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