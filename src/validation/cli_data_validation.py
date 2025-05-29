from src.utils.consts import DATA_DIR_PATH
from src.utils.file_utils import get_file
import jadnvalidation
# from jadnvalidation.jadnvalidation import DataValidation

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
        
        data = file_data[self.data_filename]
        if(isinstance(data, str)):
            try :
                # TODO: get format from user or from file extension?
                # TODO: get root from user or have data validation figure it out from schema?
                root = "Library"
                j_validation = jadnvalidation.DataValidation(schema_data, root, data, "json")
                j_validation.validate()
            except Exception as e:
                raise ValueError(f"Data Invalid - {e}")

        else:
            raise ValueError(f"Data from {self.data_filename} is not a valid.")
        
        return file_data[self.data_filename]
