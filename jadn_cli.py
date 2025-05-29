import cmd
import logging
import os
import sys
import pandas as pd
import texttable

from src.utils.file_utils import list_files, file_exists, pick_a_file
from src.utils.time_utils import get_err_report_filename, get_now
from src.validation.cli_data_validation import CliDataValidation, CliSchemaValidation
from src.utils.consts import DATA_DIR_PATH, OUTPUT_DIR_PATH, SCHEMAS_DIR_PATH

class JadnCLI(cmd.Cmd):
    
    logging.basicConfig(filename='jadn_cli_errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    error_list = []
    
    def __init__(self):
        super().__init__()

        if len(sys.argv) == 3:
            if sys.argv[1] == 'v_schema':             
                self.do_v_schema(sys.argv[2])
        if len(sys.argv) == 4:
            if sys.argv[1] == 'v_data':
                args = [sys.argv[2], sys.argv[3]]
                self.do_v_data(args)
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
        
    def do_v_schema(self, arg = None): 
        'Validate a JADN Schema. \nUpload your schema to the schemas dir. \nCommand: v_schema <schema_file_name>'
        
        j_schema = None
        
        if not arg:
            list_files(SCHEMAS_DIR_PATH)
            j_schema = pick_a_file(SCHEMAS_DIR_PATH, "Enter the schema filename to validate (or type 'exit' to cancel): ")
                    
        elif isinstance(arg, str):        
            does_exist = file_exists(SCHEMAS_DIR_PATH, arg)
            
            if not does_exist:
                print(f"Schema {arg} not found.")
                self.do_v_schema()
                return

            j_schema = arg

        elif isinstance(arg, list) and len(arg) >= 1: 
            does_exist = file_exists(SCHEMAS_DIR_PATH, arg[0])
            
            if not does_exist:
                print(f"Schema {arg} not found.")
                self.do_v_schema()
                return

            j_schema = arg[0]
            
        else:
            print("Invalid argument. Please provide a schema filename or use the list command.")
            return
        
        try:
            schema_validation = CliSchemaValidation(j_schema)
            is_valid = schema_validation.validate()
            
            if is_valid:
                print(f'Schema {j_schema} is valid.')
            else:
                print(f'Schema {j_schema} is invalid.')
            
        except Exception as e:
            print(f'An error occurred while validating the schema: {e}')
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            self.error_list.append({'timestamp': get_now(), 'error_type': type(e).__name__, 'err message': str(e)})
            
    def do_v_data(self, args):
        'Validate data against a JADN schema.  \nUpload files to the schemas and data directories. \nCommand: validate_data <schema_file> <data_file>'
        
        if isinstance(args, str):
            args = args.strip().split()
        
        # self.do_v_schema(args)

        schema_filename = args[0] if len(args) > 0 else None
        data_filename = args[1] if len(args) > 1 else None
        
        if not schema_filename:
            list_files(SCHEMAS_DIR_PATH)
            schema_filename = pick_a_file(SCHEMAS_DIR_PATH, "Enter a schema filename (or type 'exit' to cancel): ")        
        
        if not data_filename:
            list_files(DATA_DIR_PATH)
            data_filename = pick_a_file(DATA_DIR_PATH, "Enter a data filename (or type 'exit' to cancel): ")             
            
        try:
            data_validation = CliDataValidation(schema_filename, data_filename)
            is_valid = data_validation.validate()
            
            if is_valid:
                print(f'Data {data_filename} is valid.')
            else:
                print(f'Data {data_filename} is invalid.')
            
        except Exception as e:
            print(f'An error occurred while validating the data: {e}')
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            self.error_list.append({'timestamp': get_now(), 'error_type': type(e).__name__, 'err message': str(e)})

            
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
        return
            
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