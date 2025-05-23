import cmd
import glob
import logging
import os
import sys
import pandas as pd
import texttable

from src.utils.file_utils import file_exists
from src.utils.time_utils import get_err_report_filename, get_now
from src.validation.validation import SchemaValidation
from src.utils.consts import OUTPUT_DIR_PATH, SCHEMAS_DIR_PATH

class JadnCLI(cmd.Cmd):
    
    logging.basicConfig(filename='jadn_cli_errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    error_list = []
    
    def __init__(self):
        super().__init__()

        if len(sys.argv) > 1:
            if sys.argv[1] == 'v_schema' and sys.argv[2]:             
                self.do_v_schema(sys.argv[2])
        else: 
            self.intro = '''Welcome to the JSON Abstract Data Notation (JADN) CLI tool. \nView the list of commands below to get started.'''
            
        self.prompt = '(jadn) ' 

    def cmdloop(self, intro=None):
        if intro is not None:
            print(intro)
        else:
            print(self.intro)
        self.do_help("") 
        super().cmdloop(intro="")

    def do_exit(self, arg):
        'Exit the JADN CLI.'
        print('See you next time. ')
        return True

    def do_list_schemas(self, arg):
        """List all files in the schemas directory."""
        schemas_dir = os.path.join(os.getcwd(), "schemas")
        if not os.path.exists(schemas_dir):
            print("The 'schemas' directory does not exist.")
            return
        
        files = glob.glob(os.path.join(schemas_dir, "*"))
        if files:
            print("Files in 'schemas' directory:")
            for f in files:
                print("  -", os.path.basename(f))
                
            valid_filenames = [os.path.basename(f) for f in files]
            while True:
                filename = input("Enter the filename to validate (or type 'exit' to cancel): ").strip()
                if filename.lower() == 'exit':
                    print("Operation cancelled.")
                    return
                if filename in valid_filenames:
                    self.do_v_schema(filename)
                    break
                else:
                    print("Invalid filename. Please try again or type 'exit' to cancel.")               
                
        else:
            print("No files found in the 'schemas' directory.")        
        
    def do_v_schema(self, arg): 
        'Validate a JADN Schema. \nUpload your schema to the schemas dir. \nCommand: v_schema <schema_file_name>'
        
        if not arg:
            self.do_list_schemas('')           
            return
        
        does_exist = file_exists(SCHEMAS_DIR_PATH, arg)
        if not does_exist:
            print(f"Schema {arg} not found.")
            self.do_list_schemas('')           
            return        
        
        try:
            schema_validation = SchemaValidation()
            is_valid = schema_validation.validate(arg)
            
            if is_valid:
                print(f'Schema {arg} is valid.')
            
        except Exception as e:
            print(f'An error occurred while validating the schema: {e}')
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            self.error_list.append({'timestamp': get_now(), 'error_type': type(e).__name__, 'err message': str(e)})
            
    def do_v_data(self, arg):
        'Validate data against a JADN schema coming soon. \nUsage: validate_data <schema_file> <data_file>'
        if not arg:
            print('Please provide a schema filename and a data filename to validate.')
            return

            
    def do_c_schema(self, arg):
        'Convert a JADN schema to another format coming soon. \nUsage: convert_schema <schema_file> <convert_to>'
        if not arg:
            print('Please provide a schema filename and an output format.')
            return


    def do_c_data(self, arg):
        'Convert data to another format coming soon. \nUsage: data_conversion <data_file> <output_format>'
        if not arg:
            print('Please provide a data filename and an output format.')
            return

    
    def do_vis_schema(self, arg):
        'Visualize the schema ins another format coming soon. \nUsage: vis_schema <schema> <output_format>'
        if not arg:
            print('Please provide a data filename and an output format.')
            return    
            
    def do_gen_err_report(self, arg):
        if self.error_list:
            df = pd.DataFrame(self.error_list)
            filename = get_err_report_filename()
            filepath = os.path.join(OUTPUT_DIR_PATH, filename)
            df.to_csv(filepath, index=False, mode='a', header=False)
            print(f"Error report generated: {filepath}")
        else:
            print("No errors to report.")   
            
    def do_out_err_report(self, arg):
        'Read the error report.'
        filename = get_err_report_filename()
        filepath = os.path.join(OUTPUT_DIR_PATH, filename)
        
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            print(df)
        else:
            print("No error report found.")
            
    def do_version(self, arg):
        'Show the version of the JADN CLI.'
        print('JADN CLI version 1.0.0')                     
            
    def do_clear(self, arg):
        'Clear the screen.'
        print('\033c', end='')
    
    def do_help(self, arg):
      """List available commands in a table."""
      table = texttable.Texttable()
      table.header(["Command", "Description"])
      commands = [attr for attr in dir(self) if attr.startswith('do_')]
      for command in commands:
          docstring = getattr(self, command).__doc__
          command_name = command[3:]  # Remove "do_" prefix
          table.add_row([command_name, docstring or "No description available"])
      print(table.draw())    
        
    def postloop(self):
        self.do_gen_err_report('')
        
if __name__ == '__main__':
    JadnCLI().cmdloop()        