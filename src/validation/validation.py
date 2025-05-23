import json
import jadn
from src.utils.consts import SCHEMAS_DIR_PATH
from src.utils.file_utils import get_file


class SchemaValidation():
    
    schema: dict = {}
    errors: list = []
    
    def __init__(self, schema = None):
        self.schema = schema

    def validate(self, filename):
        
        file_data = get_file(SCHEMAS_DIR_PATH, filename)
        if not file_data:
            raise ValueError(f"jadn schema {filename} not found.  Double check the schema folder and filename.")
        
        if(isinstance(file_data[filename], str)):
            try:
                self.schema = json.loads(file_data[filename])
            except Exception as e:
                return False, f"Schema Invalid - {e}"
        
        jadn.check(self.schema)
        
        return True