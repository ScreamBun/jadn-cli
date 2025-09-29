import json

from jadnvalidation import DataValidation
from jadnvalidation.data_validation.schemas.jadn_meta_schema import j_meta_schema, j_meta_roots

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
                schema_data = file_data[self.schema_filename]
                
                if isinstance(schema_data, str):
                    schema_data = json.loads(schema_data)
                    
                j_validation = DataValidation(j_meta_schema, j_meta_roots, schema_data)
                j_validation.validate()                
                
            except Exception as e:
                raise ValueError(f"Schema Invalid - {e}")
        else:
            raise ValueError(f"Schema {self.schema_filename} is not a valid JSON string.")
        
        return schema_data