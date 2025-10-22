import cmd
import logging
import os
import sys
import pandas as pd
import texttable
import json

from src.logic.cli_schema_reverse_translate import SchemaReverseTranslate
from src.utils.config import get_config_value
from src.utils.file_utils import map_files, list_files, file_exists, pick_a_file, pick_an_option, update_file_extension, write_to_output
from src.utils.time_utils import get_err_report_filename, get_now
from src.logic.cli_data_validation import CliDataValidation, CliSchemaValidation
from src.utils.consts import DATA_DIR_PATH, JADN_SCHEMA_FILE_EXT, OUTPUT_DIR_PATH, SCHEMAS_DIR_PATH, VALID_SCHEMA_FORMATS, VALID_REV_SCHEMA_FORMATS, VALID_SCHEMA_VIS_FORMATS, VALID_SCHEMA_VIS_OPTIONS, GV_FILE_EXT, PLANT_UML_FILE_EXT
from src.logic.cli_schema_conversion import CliSchemaConversion

class JadnCLI(cmd.Cmd):
    
    logging.basicConfig(filename='jadn_cli_errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
    error_list = []
    
    def __init__(self):
        super().__init__()
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
        'Validate a JADN Schema. \n\nFirst, load your schema into the schemas directory, \nnext run the command: \n\npython jadn_cli.py schema_v <schema_filename>'        
        
        j_schema = None
        if not arg:
            list_files(SCHEMAS_DIR_PATH)
            j_schema = pick_a_file(SCHEMAS_DIR_PATH, "Enter a number or schema filename to validate (or type 'exit' to cancel): ")
        
        elif arg.isdigit():        
            file_map = map_files(SCHEMAS_DIR_PATH)
            try: 
                j_schema = file_map[int(arg)].split('/')[-1]
                
            except:
                print(f"Schema not found")
                self.do_schema_v()
                return

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
            
    def do_data_c(self, args):
        'Convert JSON Verbose Data into JSON Concise Data.\n\npython jadn_cli.py data_c [data_filename] [-b --bulk]'
        if isinstance(args, str):
            args = args.strip().split()

        data_filename = args[0] if len(args) > 0 else None
        bulk = data_filename == '-b' or data_filename == '--bulk'

        data_map = {}

        use_prompts = get_config_value("use_prompts", True)
        if not use_prompts: 
            if not data_filename and not bulk:
                print("Error: Commands missing. Use 'python jadn_cli.py data_c <data_filename.json>'")
                sys.exit(1)
        
        if not data_filename and not bulk:
            list_files(DATA_DIR_PATH, is_jadn_only=False, is_json_only=True)
            data_filename = pick_a_file(DATA_DIR_PATH, is_jadn_only=False, is_json_only=True, prompt="Enter a number or data filename (or type 'exit' to cancel): ")
        elif data_filename.isdigit() and not bulk:
            data_map = map_files(DATA_DIR_PATH, is_jadn_only=False, is_json_only=True)
            try:
                data_filename = data_map[int(data_filename)].split('/')[-1]
            except:
                print(f"Data {data_filename} not found.")
                self.do_data_c(args = [])
                return

        try:
            if bulk:
                directory = DATA_DIR_PATH
                extension = '.json'

                for data_filename in os.listdir(directory):
                    if data_filename.endswith(extension):
                        read_data = json.loads(open(os.path.join(DATA_DIR_PATH, data_filename), 'r').read())
                        concise_data = json.dumps(read_data)
                        new_filename = update_file_extension(data_filename, 'json')
                        write_to_output(new_filename, concise_data)
                        print(f' - Data {data_filename} has been converted to concise format.')
                return
            else:
                read_data = json.loads(open(os.path.join(DATA_DIR_PATH, data_filename), 'r').read())
                concise_data = json.dumps(read_data)
                new_filename = update_file_extension(data_filename, 'json')
                write_to_output(new_filename, concise_data)
                print(f' - Data {data_filename} has been converted to concise format.')
        except Exception as e:
            print(f' - An error occurred while converting the data: {e}')
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            self.error_list.append({'timestamp': get_now(), 'error_type': type(e).__name__, 'err message': str(e)})

    def do_data_v(self, args):
        'Validate data against a JADN schema. \n\nFirst, load your schema into the schemas directory, \nnext load your data file to the data directory, and \nthen, run the command: \n\npython jadn_cli.py data_v <schema_filename> <data_filename>'
        
        if isinstance(args, str):
            args = args.strip().split()

        schema_filename = args[0] if len(args) > 0 else None
        data_filename = args[1] if len(args) > 1 else None

        schema_map = {}
        data_map = {}
        
        use_prompts = get_config_value("use_prompts", True)
        if not use_prompts: 
            if not schema_filename or not data_filename:
                print("Error: Commands missing. Use 'python jadn_cli.py data_v <schema_file> <data_filename>'")
                sys.exit(1)          
        
        use_prompts = get_config_value("use_prompts", True)
        if not use_prompts: 
            if not schema_filename or not data_filename:
                print("Error: Commands missing. Use 'python jadn_cli.py data_v <schema_file> <data_filename>'")
                sys.exit(1)          
        
        if not schema_filename:
            list_files(SCHEMAS_DIR_PATH)
            schema_filename = pick_a_file(SCHEMAS_DIR_PATH, prompt="Enter a number or schema filename (or type 'exit' to cancel): ")  
        elif schema_filename.isdigit():
            schema_map = map_files(SCHEMAS_DIR_PATH) 
            try:     
                schema_filename = schema_map[int(schema_filename)].split('/')[-1]
            except:
                print(f"Schema {schema_filename} not found.")
                self.do_data_v(args = [])
                return
        
        if not data_filename:
            list_files(DATA_DIR_PATH, is_jadn_only=False)
            data_filename = pick_a_file(DATA_DIR_PATH, is_jadn_only=False, prompt="Enter a number or data filename (or type 'exit' to cancel): ")
        elif data_filename.isdigit():
            data_map = map_files(DATA_DIR_PATH, is_jadn_only=False)
            try:
                data_filename = data_map[int(data_filename)].split('/')[-1]
            except:
                print(f"Data {data_filename} not found.")
                self.do_data_v(args = [])
                return
            
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
        'Translate a JADN Schema to a JIDL, JSON Schema or an XSD. \n\nFirst, load your schema into the schemas directory, \nnext run the command: \n\npython jadn_cli.py schema_t <schema_filename> <jidl, json, or xsd>'

        if isinstance(args, str):
            args = args.strip().split()

        schema_filename = args[0] if len(args) > 0 else None
        convert_to = args[1] if len(args) > 1 else None

        schema_map = {}
        
        use_prompts = get_config_value("use_prompts", True)
        if not use_prompts: 
            if not schema_filename or not convert_to:
                print("Error: Commands missing. Use 'python jadn_cli.py schema_t <schema_file> <convert_to>'")
                sys.exit(1)            
        
        use_prompts = get_config_value("use_prompts", True)
        if not use_prompts: 
            if not schema_filename or not convert_to:
                print("Error: Commands missing. Use 'python jadn_cli.py schema_t <schema_file> <convert_to>'")
                sys.exit(1)            
        
        if not schema_filename:
            list_files(SCHEMAS_DIR_PATH)
            schema_filename = pick_a_file(SCHEMAS_DIR_PATH, "Enter a number or schema filename (or type 'exit' to cancel): ")        
        
            if schema_filename is None:
                return
        elif schema_filename.isdigit():
            schema_map = map_files(SCHEMAS_DIR_PATH) 
            try:     
                schema_filename = schema_map[int(schema_filename)].split('/')[-1]
            except:
                print(f"Schema {schema_filename} not found.")
                self.do_schema_t(args = [])
                return
        
        if not convert_to:
            convert_to = pick_an_option(VALID_SCHEMA_FORMATS, opts_title="Schema Formats:", prompt="Enter a format to convert the schema to: ")
            if convert_to is None:
                return
        elif convert_to.isdigit():
            try:
                convert_to = VALID_SCHEMA_FORMATS[int(convert_to) - 1]
            except IndexError:
                print(f"Invalid format number: {convert_to}")
                self.do_schema_t(args = [])
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

    def do_schema_t_bulk(self, args):
        'Translate all JADN Schemas to JIDL, JSON Schemas or XSD. \n\nFirst, load your schemas into the schemas directory, \nnext run the command: \n\npython jadn_cli.py schema_t_bulk <jidl, json, or xsd>'

        if isinstance(args, str):
            args = args.strip().split()

        convert_to = args[0] if len(args) > 0 else None

        schema_map = {} 

        use_prompts = get_config_value("use_prompts", True)
        if not use_prompts: 
            if not convert_to:
                print("Error: Commands missing. Use 'python jadn_cli.py schema_t_bulk <convert_to>'")
                sys.exit(1)                    
        
        if not convert_to:
            convert_to = pick_an_option(VALID_SCHEMA_FORMATS, opts_title="Schema Formats:", prompt="Enter a format to convert the schemas to: ")
            if convert_to is None:
                return
        elif convert_to.isdigit():
            try:
                convert_to = VALID_SCHEMA_FORMATS[int(convert_to) - 1]
            except IndexError:
                print(f"Invalid format number: {convert_to}")
                self.do_schema_t(args = [])
                return

        directory = SCHEMAS_DIR_PATH
        extension = JADN_SCHEMA_FILE_EXT

        for schema_filename in os.listdir(directory):
            if schema_filename.endswith(extension):
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
        'Reverse translate JIDL or JSON Schema into a JADN Schema. \n\nFirst, load your schema into the schemas directory, \nnext run the command: \n\npython jadn_cli.py schema_rev_t <schema_filename>'

        if isinstance(args, str):
            args = args.strip().split()

        filename = args[0] if len(args) > 0 else None
        schemas_map = {}
        
        use_prompts = get_config_value("use_prompts", True)
        if not use_prompts: 
            if not filename:
                print("Error: Commands missing. Use 'python jadn_cli.py schema_rev_t <schema_file>'")
                sys.exit(1)          
        
        use_prompts = get_config_value("use_prompts", True)
        if not use_prompts: 
            if not filename:
                print("Error: Commands missing. Use 'python jadn_cli.py schema_rev_t <schema_file>'")
                sys.exit(1)          
        
        if not filename:
            list_files(SCHEMAS_DIR_PATH, is_jadn_only=False)
            filename = pick_a_file(SCHEMAS_DIR_PATH, is_jadn_only=False, prompt="Enter a schema by name or number (type 'exit' to cancel): ")        
        
            if filename is None:
                return
        elif filename.isdigit():
            schemas_map = map_files(SCHEMAS_DIR_PATH, is_jadn_only=False) 
            try:     
                filename = schemas_map[int(filename)].split('/')[-1]
            except:
                print(f"Schema {filename} not found.")
                self.do_schema_rev_t(args = [])
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

    def do_schema_rev_t_bulk(self, args):
        'Reverse translate all JIDL or JSON Schemas into a JADN Schema. \n\nFirst, load your schema into the data directory, \nnext run the command: \n\npython jadn_cli.py schema_rev_t <jidl, json>'

        if isinstance(args, str):
            args = args.strip().split()

        convert_to = args[0] if len(args) > 0 else None

        schema_map = {} 

        use_prompts = get_config_value("use_prompts", True)
        if not use_prompts: 
            if not convert_to:
                print("Error: Commands missing. Use 'python jadn_cli.py schema_rev_t_bulk <convert_to>'")
                sys.exit(1)                    
        
        if not convert_to:
            convert_to = pick_an_option(VALID_REV_SCHEMA_FORMATS, opts_title="Schema Formats:", prompt="Enter a format to convert the schemas to: ")
            if convert_to is None:
                return
        elif convert_to.isdigit():
            try:
                convert_to = VALID_SCHEMA_FORMATS[int(convert_to) - 1]
            except IndexError:
                print(f"Invalid format number: {convert_to}")
                self.do_schema_t(args = [])
                return

        directory = SCHEMAS_DIR_PATH
        extension = f'.{convert_to}'

        for schema_filename in os.listdir(directory):
            if schema_filename.endswith(extension):
                try:
                    rev_translate = SchemaReverseTranslate(schema_filename)
                    file_translated = rev_translate.translate()
                    
                    if file_translated:
                        print(f'  - {schema_filename} has been reverse translated into a JADN Schema.')
                        new_filename = update_file_extension(schema_filename, JADN_SCHEMA_FILE_EXT)
                        write_to_output(new_filename, file_translated)
                    else: 
                        print(f'  - {schema_filename} could not be reverse translated into a JADN Schema.')

                except Exception as e:
                    print(f'  - An error occurred while reverse translating {schema_filename} to {JADN_SCHEMA_FILE_EXT}: {e}')
                    logging.error(f"An error occurred: {str(e)}", exc_info=True)
                    self.error_list.append({'timestamp': get_now(), 'error_type': type(e).__name__, 'err message': str(e)})       
            
    def do_schema_vis(self, args):
        'Convert a JADN Schema into a visual representation, such as MarkDown, HTML, GraphViz or PlantUML. \n\nFirst, load your schema into the schemas directory, \nnext, run the command: \n\npython jadn_cli.py schema_vis <schema_filename> <md, html, gv, or puml>'

        if isinstance(args, str):
            args = args.strip().split()

        schema_filename = args[0] if len(args) > 0 else None
        convert_to = args[1] if len(args) > 1 else None
        vis_opt = args[2] if len(args) > 2 else None
        
        schema_map = {}

        use_prompts = get_config_value("use_prompts", True)
        if not use_prompts: 
            if not schema_filename or not convert_to:
                print("Error: Commands missing. Use 'python jadn_cli.py schema_vis <schema_file> <convert_to>'")
                sys.exit(1)        
        
        if not schema_filename:
            list_files(SCHEMAS_DIR_PATH)
            schema_filename = pick_a_file(SCHEMAS_DIR_PATH, "Enter a number or schema filename (or type 'exit' to cancel): ")        
        
            if schema_filename is None:
                return
        elif schema_filename.isdigit():
            schema_map = map_files(SCHEMAS_DIR_PATH) 
            try:     
                schema_filename = schema_map[int(schema_filename)].split('/')[-1]
            except:
                print(f"Schema {schema_filename} not found.")
                self.do_schema_vis(args = [])
                return
        
        if not convert_to:
            convert_to = pick_an_option(VALID_SCHEMA_VIS_FORMATS, opts_title="Schema Visualization Formats:", prompt="Enter a format to convert the schema to: ")
            if convert_to is None:
                return
        elif convert_to.isdigit():
            try:
                convert_to = VALID_SCHEMA_VIS_FORMATS[int(convert_to) - 1]
            except IndexError:
                print(f"Invalid format number: {convert_to}")
                self.do_schema_vis(args = [])
                return

        if convert_to == GV_FILE_EXT or convert_to == PLANT_UML_FILE_EXT:
            if ((vis_opt not in VALID_SCHEMA_VIS_OPTIONS) and not (vis_opt and vis_opt.isdigit() and (1 <= int(vis_opt) <= len(VALID_SCHEMA_VIS_OPTIONS)))):
                vis_opt = pick_an_option(VALID_SCHEMA_VIS_OPTIONS, opts_title="Visualization Options (Default = information):", prompt="Enter an option for the visualization: ")
                if vis_opt is None:
                    return
            elif vis_opt.isdigit():
                try:
                    vis_opt = VALID_SCHEMA_VIS_OPTIONS[int(vis_opt) - 1]
                except IndexError:
                    print(f"Invalid option number: {vis_opt}")
                    self.do_schema_vis(args = [])
                    return
        else:
            vis_opt = None
            
        try:
            schema_conversion = CliSchemaConversion(schema_filename, convert_to)
            schema_converted = schema_conversion.convert(vis_opt)
            
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
        'This command will generate a CSV file in the output directory with all errors logged during the session.'
        if self.error_list:
            df = pd.DataFrame(self.error_list)
            filename = get_err_report_filename()
            filepath = os.path.join(OUTPUT_DIR_PATH, filename)
            df.to_csv(filepath, index=False, mode='a', header=False)
            print(f"Error report generated: {filepath}")
        return
            
    def do_err_report_out(self, arg):
        'Display the error report generated by the last session.'
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
        directory = OUTPUT_DIR_PATH
        extension = '.csv'

        for filename in os.listdir(directory):
            if filename.endswith(extension):
                file_path = os.path.join(directory, filename)
                os.remove(file_path)
        
        print("Cleared error reports.")

    def do_view_file(self, args):
        'View the contents of a schema or data file.\n\npython jadn_cli.py view_file <filename> [option]\n\nOptions:\n--code: open file in VSCode\n--vim: open file in Vim\n--head: display first 10 lines\n--tail: display last 10 lines'
        if isinstance(args, str):
            args = args.strip().split()

        filename = args[0] if len(args) > 0 else None
        option = args[1] if len(args) > 1 else None
        files_map = {}

        use_prompts = get_config_value("use_prompts", True)
        if not use_prompts: 
            if not filename:
                print("Error: Commands missing. Use 'python jadn_cli.py view_file <filename> [option]'")
                sys.exit(1)

        try: 
            if not filename:
                list1 = list_files(SCHEMAS_DIR_PATH, is_jadn_only=False, join_list=[])
                list2 = list_files(DATA_DIR_PATH, is_jadn_only=False, join_list=list1)
                filename = pick_a_file('.', fromArray=list2, is_jadn_only=False, is_json_only=False, prompt="Enter a number or filename to view (or type 'exit' to cancel): ")

            if not option:
                option = pick_an_option(['None', '--code', '--vim', '--head', '--tail'], opts_title="View Options:", prompt="Enter an option to view the file (default = cat): ")
            
            if option == '--code':
                os.system('code ' + filename)
            elif option == '--vim':
                os.system('vim ' + filename)
            elif option == '--head':
                os.system('head -n 10 ' + filename)
                print("\n")
            elif option == '--tail':
                os.system('tail -n 10 ' + filename)
                print("\n")
            else:
                os.system('cat ' + filename)
                print("\n")

        except Exception as e:
            print(f"An error occurred while trying to view the file: {e}")
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            self.error_list.append({'timestamp': get_now(), 'error_type': type(e).__name__, 'err message': str(e)})
        
        return

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
        use_prompts = get_config_value("use_prompts", True)
        if use_prompts:
            cli.cmdloop()  
        else:
            print("No command provided. Use 'jadn_cli.py help' to see available commands.")
            sys.exit(1)