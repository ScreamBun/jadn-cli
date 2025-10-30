import json
from src.utils.consts import COMPACT_CONST, CONCISE_CONST, DATA_DIR_PATH, SCHEMAS_DIR_PATH, JSON_FILE_EXT
from src.utils.file_utils import get_file
from jadnutils.json.convert_compact import convert_to_compact
from jadnutils.json.convert_concise import convert_to_concise

class CliDataConversion():
    
    schema_filename: str = None
    data_filename: str = None
    convert_to: str = None
    errors: list = []
    
    def __init__(self, schema_filename: str, data_filename: str, convert_to: str = None):
        self.schema_filename = schema_filename
        self.data_filename = data_filename
        self.convert_to = convert_to

    def convert(self, opt = None):
        converted_data = None

        schema_file_data = get_file(SCHEMAS_DIR_PATH, self.schema_filename)
        if not schema_file_data:
            raise ValueError(f"Schema {self.schema_filename} not found.  Double check the schemas folder and filename.")

        data_file_data = get_file(DATA_DIR_PATH, self.data_filename)
        if not data_file_data:
            raise ValueError(f"JSON Data {self.data_filename} not found.  Double check the data folder and filename.")
        
        try:
            schema_data_str = schema_file_data[self.schema_filename]
            schema_data = json.loads(schema_data_str) # Ensure it's a valid JSON string

            data_data_str = data_file_data[self.data_filename]
            data_data = json.loads(data_data_str, ) # Ensure it's a valid JSON string
             
            if self.convert_to == COMPACT_CONST:
                converted_data = convert_to_compact(schema_data, data_data)
            
            elif self.convert_to == CONCISE_CONST:
                converted_data = convert_to_concise(schema_data, data_data)

            converted_data = json.dumps(converted_data, indent=4) if converted_data else None
                
        except Exception as e:
            raise ValueError(f"Data Invalid - {e}")
        
        return converted_data