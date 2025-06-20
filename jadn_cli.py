import cmd
import logging
import os
import sys
import pandas as pd
import texttable

from src.logic.cli_schema_reverse_translate import SchemaReverseTranslate
from src.utils.file_utils import list_files, file_exists, pick_a_file, pick_an_option, update_file_extension, write_to_output
from src.utils.time_utils import get_err_report_filename, get_now
from src.logic.cli_data_validation import CliDataValidation, CliSchemaValidation
from src.utils.consts import DATA_DIR_PATH, JADN_SCHEMA_FILE_EXT, OUTPUT_DIR_PATH, SCHEMAS_DIR_PATH, VALID_SCHEMA_FORMATS, VALID_SCHEMA_VIS_FORMATS
from src.logic.cli_schema_conversion import CliSchemaConversion

class JadnCLI(cmd.Cmd):
    
    logging.basicConfig(filename='jadn_cli_errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
    error_list = []
    
    def __init__(self):
        super().__init__()

        if len(sys.argv) == 3:
            if sys.argv[1] == 'schema_v':             
                self.do_schema_v(sys.argv[2])
        if len(sys.argv) == 4:
            if sys.argv[1] == 'data_v':
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
        print('Thank you for using JADN. ')
        return True      
        
    def do_schema_v(self, arg = None): 
        'Validate a JADN Schema. \nUpload your schema to the schemas dir. \nCommand: schema_v <schema_file_name>'
        
        j_schema = None
        
        if not arg:
            list_files(SCHEMAS_DIR_PATH)
            j_schema = pick_a_file(SCHEMAS_DIR_PATH, "Enter a number or schema filename to validate (or type 'exit' to cancel): ")
                    
        elif isinstance(arg, str):        
            does_exist = file_exists(SCHEMAS_DIR_PATH, arg)
            
            if not does_exist:
                print(f"Schema {arg} not found.")
                self.do_schema_v()
                return

            j_schema = arg

        elif isinstance(arg, list) and len(arg) >= 1: 
            does_exist = file_exists(SCHEMAS_DIR_PATH, arg[0])
            
            if not does_exist:
                print(f"Schema {arg} not found.")
                self.do_schema_v()
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
            
    def do_data_v(self, args):
        'Validate data against a JADN schema.  \nUpload files to the schemas and data directories. \nCommand: v_data <schema_file> <data_file>'
        
        if isinstance(args, str):
            args = args.strip().split()

        schema_filename = args[0] if len(args) > 0 else None
        data_filename = args[1] if len(args) > 1 else None
        
        if not schema_filename:
            list_files(SCHEMAS_DIR_PATH)
            schema_filename = pick_a_file(SCHEMAS_DIR_PATH, prompt="Enter a number or schema filename (or type 'exit' to cancel): ")        
        
        if not data_filename:
            list_files(DATA_DIR_PATH, is_jadn_only=False)
            data_filename = pick_a_file(DATA_DIR_PATH, is_jadn_only=False, prompt="Enter a number or data filename (or type 'exit' to cancel): ")
            
        try:
            data_validation = CliDataValidation(schema_filename, data_filename)
            is_valid = data_validation.validate()
            
            if is_valid:
                print(f' - Data {data_filename} is valid.')
            else:
                print(f' - Data {data_filename} is invalid.')
            
        except Exception as e:
            print(f' - An error occurred while validating the data: {e}')
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            self.error_list.append({'timestamp': get_now(), 'error_type': type(e).__name__, 'err message': str(e)})

    def do_schema_t(self, args):
        'Translate a JADN Schema to a JIDL, JSON Schema or an XSD. \nUsage: schema_t <schema_file> <convert_to>'

        if isinstance(args, str):
            args = args.strip().split()

        schema_filename = args[0] if len(args) > 0 else None
        convert_to = args[1] if len(args) > 1 else None
        
        if not schema_filename:
            list_files(SCHEMAS_DIR_PATH)
            schema_filename = pick_a_file(SCHEMAS_DIR_PATH, "Enter a number or schema filename (or type 'exit' to cancel): ")        
        
            if schema_filename is None:
                return
        
        if not convert_to:
            convert_to = pick_an_option(VALID_SCHEMA_FORMATS, opts_title="Schema Formats:", prompt="Enter a format to convert the schema to: ")
            if convert_to is None:
                return
            
        try:
            schema_conversion = CliSchemaConversion(schema_filename, convert_to)
            schema_converted = schema_conversion.convert()
            
            if schema_converted:
                print(f' - Schema {schema_filename} has been converted to {convert_to}.')
                new_filename = update_file_extension(schema_filename, convert_to)
                write_to_output(new_filename, schema_converted)
            else: 
                print(f' - Schema {schema_filename} could not be converted to {convert_to}.')
            
        except Exception as e:
            print(f' - An error occurred while converting {schema_filename} to {convert_to}: {e}')
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            self.error_list.append({'timestamp': get_now(), 'error_type': type(e).__name__, 'err message': str(e)})
            
    def do_schema_rev_t(self, args):
        'Reverse translate JIDL or JSON Schema into a JADN Schema. \nUsage: schema <schema_file>'

        if isinstance(args, str):
            args = args.strip().split()

        filename = args[0] if len(args) > 0 else None
        
        if not filename:
            list_files(SCHEMAS_DIR_PATH, is_jadn_only=False)
            filename = pick_a_file(SCHEMAS_DIR_PATH, is_jadn_only=False, prompt="Enter a schema by name or number (type 'exit' to cancel): ")        
        
            if filename is None:
                return
            
        try:
            rev_translate = SchemaReverseTranslate(filename)
            file_translated = rev_translate.translate()
            
            if file_translated:
                print(f'  - {filename} has been reverse translated into a JADN Schema.')
                new_filename = update_file_extension(filename, JADN_SCHEMA_FILE_EXT)
                write_to_output(new_filename, file_translated)
            else: 
                print(f'  - {filename} could not be reverse translated into a JADN Schema.')
            
        except Exception as e:
            print(f'  - An error occurred while reverse translating {filename} to {JADN_SCHEMA_FILE_EXT}: {e}')
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            self.error_list.append({'timestamp': get_now(), 'error_type': type(e).__name__, 'err message': str(e)})            
            
    def do_schema_vis(self, args):
        'Convert a JADN Schema to a visual representation,such as MarkDown, HTML, GraphViz or PlantUML. \nUsage: schema_vis <schema_file> <convert_to>'

        if isinstance(args, str):
            args = args.strip().split()

        schema_filename = args[0] if len(args) > 0 else None
        convert_to = args[1] if len(args) > 1 else None
        
        if not schema_filename:
            list_files(SCHEMAS_DIR_PATH)
            schema_filename = pick_a_file(SCHEMAS_DIR_PATH, "Enter a number or schema filename (or type 'exit' to cancel): ")        
        
            if schema_filename is None:
                return
        
        if not convert_to:
            convert_to = pick_an_option(VALID_SCHEMA_VIS_FORMATS, opts_title="Schema Visualization Formats:", prompt="Enter a format to convert the schema to: ")
            if convert_to is None:
                return
            
        try:
            schema_conversion = CliSchemaConversion(schema_filename, convert_to)
            schema_converted = schema_conversion.convert()
            
            if schema_converted:
                print(f' - Schema {schema_filename} has been converted to {convert_to}.')
                new_filename = update_file_extension(schema_filename, convert_to)
                write_to_output(new_filename, schema_converted)
            else: 
                print(f' - Schema {schema_filename} could not be converted to {convert_to}.')
            
        except Exception as e:
            print(f' - An error occurred while converting {schema_filename} to {convert_to}: {e}')
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            self.error_list.append({'timestamp': get_now(), 'error_type': type(e).__name__, 'err message': str(e)})              
            
    def do_err_report_gen(self, arg):
        if self.error_list:
            df = pd.DataFrame(self.error_list)
            filename = get_err_report_filename()
            filepath = os.path.join(OUTPUT_DIR_PATH, filename)
            df.to_csv(filepath, index=False, mode='a', header=False)
            print(f"Error report generated: {filepath}")
        return
            
    def do_err_report_out(self, arg):
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

    def do_clear_log(self, arg = None):
        'Clear the error log. \nPast errors will not be reflected in generated error reports.'
        
        filepath = os.path.join('jadn_cli_errors.log')
        if os.path.exists(filepath):
            self.error_list = []
            with open(filepath, "r+") as log:
                log.truncate(0)
            print("Error log cleared.")
        else:
            print("No error log found.")
    
    def do_clear_reports(self, arg = None):
        'Clear all generated error reports.'
        directory = 'output'
        extension = '.csv'

        for filename in os.listdir(directory):
            if filename.endswith(extension):
                file_path = os.path.join(directory, filename)
                os.remove(file_path)
        
        print("Cleared error reports.")

    def do_man(self, arg):
        """List available commands in a table."""
        self.do_help(arg)
    
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
      
    def do_about(self, arg):
        """List information and references about the JADN CLI."""
        table = texttable.Texttable()
        # table.header(["", ""])
        table.add_row(["JADN CLI", "A command-line interface for working with JADN schemas and data."])
        table.add_row(["Version", "1.0.0"]) 
        table.add_row(["JADN 2.0 OASIS Spec", "https://docs.oasis-open.org/openc2/imjadn/v2.0/imjadn-v2.0.html"])
        table.add_row(["JADN PyPi", "https://pypi.org/project/jadn/"])
        print(table.draw())        
        
    def postloop(self):
        self.do_err_report_gen('')
        
if __name__ == '__main__':
    cli = JadnCLI()
    # If command-line arguments are provided, try to execute the corresponding command
    if len(sys.argv) > 1:
        cmd_name = sys.argv[1]
        args = sys.argv[2:]
        method = getattr(cli, f'do_{cmd_name}', None)
        if method:
            # Join args as a string for consistency with cmd.Cmd
            arg_str = " ".join(args)
            method(arg_str)
        else:
            print(f"Unknown command: {cmd_name}")
        # Optionally, exit after running the command
        # sys.exit(0)
    else:
        cli.cmdloop()