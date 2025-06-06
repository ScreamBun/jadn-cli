import json
import jadn

from jadnschema.convert import json_to_jadn_dumps
from src.utils.consts import JIDL_FILE_EXT, JSON_FILE_EXT, SCHEMAS_DIR_PATH, VALID_REV_SCHEMA_TRANSLATION_FORMATS
from src.utils.file_utils import determine_file_type, get_file

class SchemaReverseTranslate():
    
    schema_filename: str = None
    errors: list = []
    
    def __init__(self, schema_filename: str):
        self.schema_filename = schema_filename

    def translate(self):
        converted_schema = None
        
        schema_file_data = get_file(SCHEMAS_DIR_PATH, self.schema_filename)
        if not schema_file_data:
            raise ValueError(f"jadn schema {self.schema_filename} not found.  Double check the schema folder and filename.")
        
        schema_type = determine_file_type(self.schema_filename)
        if schema_type not in VALID_REV_SCHEMA_TRANSLATION_FORMATS:
            raise ValueError(f"Unsupported schema format: {schema_type}. Supported formats are: {VALID_REV_SCHEMA_TRANSLATION_FORMATS}")
        
        try:
            schema_data_str = schema_file_data[self.schema_filename]
            
            if schema_type == JIDL_FILE_EXT:
                converted_schema = jadn.convert.jidl_loads(schema_data_str)
            
            elif schema_type == JSON_FILE_EXT:
                schema_data = json.loads(schema_data_str) # Ensure it's a valid JSON string
                kwargs = { "fmt": schema_type,}
                converted_schema = json_to_jadn_dumps(schema_data, **kwargs)
                converted_schema = jadn.translate.jsonschema_w.json_schema_dumps(converted_schema)
                
        except Exception as e:
            raise ValueError(f"Schema Invalid - {e}")
        
        return converted_schema