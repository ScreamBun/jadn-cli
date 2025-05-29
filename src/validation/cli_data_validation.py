import jadnvalidation

from src.utils.consts import DATA_DIR_PATH, VALID_DATA_FORMATS
from src.utils.file_utils import determine_file_type, get_file
from src.utils.gen_utils import get_schema_roots
from src.validation.cli_schema_validation import CliSchemaValidation


class CliDataValidation():
    
    schema_filename: str = None
    data_filename: str = None
    errors: list = []
    
    def __init__(self, schema_filename, data_filename):
        self.schema_filename = schema_filename
        self.data_filename = data_filename

    def validate(self):
        schema_validation = CliSchemaValidation(self.schema_filename)
        schema_data = schema_validation.validate() 
        
        if schema_data is None:
            raise ValueError(f"Schema {self.schema_filename} is not valid.  Cannot validate data without a valid schema.")
        
        file_data = get_file(DATA_DIR_PATH, self.data_filename)
        if not file_data:
            raise ValueError(f"data for {self.data_filename} not found.  Double check the data folder and filename.")
        
        roots = get_schema_roots(schema_data)
        if not roots:
            raise ValueError(f"Schema {self.schema_filename} does not have a valid root.  Cannot validate data without a valid root.")
        
        file_format = determine_file_type(self.data_filename)
        if file_format not in VALID_DATA_FORMATS:
            raise ValueError(f"Unsupported data format: {format}. Supported formats are: {VALID_DATA_FORMATS}")
        
        data = file_data[self.data_filename]
        if(isinstance(data, str)):
            for root_item in roots:
                try :
                    j_validation = jadnvalidation.DataValidation(schema_data, root_item, data, file_format)
                    j_validation.validate()
                except Exception as e:
                    raise ValueError(f"Data Invalid - {e}")

        else:
            raise ValueError(f"Data from {self.data_filename} is not a valid.")
        
        return file_data[self.data_filename]
