import json
from src.utils.consts import COMPACT_CONST, CONCISE_CONST, DATA_DIR_PATH, JSON_FILE_EXT
from src.utils.file_utils import get_file
from jadnutils.json.convert_compact import convert_to_compact

class CliDataConversion():
    
    data_filename: str = None
    convert_to: str = None
    errors: list = []
    
    def __init__(self, data_filename: str, convert_to: str = None):
        self.data_filename = data_filename
        self.convert_to = convert_to

    def convert(self, opt = None):
        converted_data = None

        data_file_data = get_file(DATA_DIR_PATH, self.data_filename)
        if not data_file_data:
            raise ValueError(f"JSON Data {self.data_filename} not found.  Double check the data folder and filename.")
        
        try:
            data_data_str = data_file_data[self.data_filename]
            data_data = json.loads(data_data_str) # Ensure it's a valid JSON string
             
            if self.convert_to == COMPACT_CONST:
                converted_data = convert_to_compact(data_data)
            
            elif self.convert_to == JSON_FILE_EXT:
                pass
                
        except Exception as e:
            raise ValueError(f"Data Invalid - {e}")
        
        return converted_data