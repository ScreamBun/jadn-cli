import json
import jadn
from src.utils.consts import SCHEMAS_DIR_PATH
from src.utils.file_utils import get_file

class CliSchemaValidation():
    
    schema_filename: str = None
    errors: list = []
    
    def __init__(self, schema_filename: str):
        self.schema_filename = schema_filename

    def validate(self):
        schema_data = None
        
        file_data = get_file(SCHEMAS_DIR_PATH, self.schema_filename)
        if not file_data:
            raise ValueError(f"jadn schema {self.schema_filename} not found.  Double check the schema folder and filename.")
        
        if(isinstance(file_data[self.schema_filename], str)):
            try:
                schema_str = file_data[self.schema_filename]
                schema_data = json.loads(schema_str) # Ensure it's a valid JSON string
                # TODO: Add schema validation check here when ready from jadn2 or sb jadn validation
                # jadn.check(schema_data) # Ensure it's a valid JADN schema
            except Exception as e:
                raise ValueError(f"Schema Invalid - {e}")
        else:
            raise ValueError(f"Schema {self.schema_filename} is not a valid JSON string.")
        
        return schema_data