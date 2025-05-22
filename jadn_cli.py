import cmd
import sys

from src.validation.validation import SchemaValidation

class JadnCLI(cmd.Cmd):
    
    
    def __init__(self):
        super().__init__()  # Call the parent class's __init__

        if len(sys.argv) > 1:
            if sys.argv[1] == 'v_schema' and sys.argv[2]:             
                self.do_v_schema(sys.argv[2])
        else: 
            self.intro = 'Welcome to the JSON Abstract Data Notation (JADN) CLI tool. Type help or ? to list commands.\n'
            
        self.prompt = '(jadn) ' 

    def do_exit(self, arg):
        'Exit the JADN CLI.'
        print('See you next time. ')
        return True
        
    def do_v_schema(self, arg): 
        'Validate a JADN schema coming soon. Usage: validate_schema <schema_file>'
        if not arg:
            print('Please provide a JADN schema filename to validate.  \nJADN schemas should be dropped in the schema folder and \nshoud have a .jadn file extension.')
            return
        
        try:
            schema_validation = SchemaValidation()
            is_valid = schema_validation.validate(arg)
            
            if is_valid:
                print(f'Schema {arg} is valid.')
            
        except Exception as e:
            print(f'An error occurred while validating the schema: {e}')
            
    def do_v_data(self, arg):
        'Validate data against a JADN schema coming soon. Usage: validate_data <schema_file> <data_file>'
        if not arg:
            print('Please provide a schema filename and a data filename to validate.')
            return
        # try:
        #     schema_file, data_file = arg.split()
        #     with open(schema_file, 'r') as f:
        #         schema = f.read()
        #     with open(data_file, 'r') as f:
        #         data = f.read()
        #         # Placeholder for actual validation logic
        #         print(f'Data in {data_file} is valid against schema {schema_file}.')
        # except FileNotFoundError:
        #     print(f'File {arg} not found.')
        # except Exception as e:
        #     print(f'An error occurred while validating the data: {e}')
            
    def do_c_schema(self, arg):
        'Convert a JADN schema to another format coming soon. Usage: convert_schema <schema_file> <convert_to>'
        if not arg:
            print('Please provide a schema filename and an output format.')
            return
        # try:
        #     schema_file, output_format = arg.split()
        #     with open(schema_file, 'r') as f:
        #         schema = f.read()
        #         # Placeholder for actual conversion logic
        #         print(f'Schema {schema_file} converted to {output_format}.')
        # except FileNotFoundError:
        #     print(f'File {arg} not found.')
        # except Exception as e:
        #     print(f'An error occurred while converting the schema: {e}')

    def do_c_data(self, arg):
        'Convert data to another format coming soon. Usage: data_conversion <data_file> <output_format>'
        if not arg:
            print('Please provide a data filename and an output format.')
            return
    #     try:
    #         data_file, output_format = arg.split()
    #         with open(data_file, 'r') as f:
    #             data = f.read()
    #             # Placeholder for actual conversion logic
    #             print(f'Data in {data_file} converted to {output_format}.')
    #     except FileNotFoundError:
    #         print(f'File {arg} not found.')
    #     except Exception as e:
    #         print(f'An error occurred while converting the data: {e}')
        
    # def do_add(self, arg):
    #     'Add two numbers. Usage: add <num1> <num2>'
    #     try:
    #         num1, num2 = map(int, arg.split())
    #         print(f'The sum is: {num1 + num2}')
    #     except ValueError:
    #         print('Invalid input. Please provide two numbers.')
    
    def do_vis_schema(self, arg):
        'Visualize the schema ins another format coming soon. Usage: vis_schema <schema> <output_format>'
        if not arg:
            print('Please provide a data filename and an output format.')
            return    
            
            
    def do_clear(self, arg):
        'Clear the screen.'
        print('\033c', end='')
        
    def do_help(self, arg):
        'List available commands.'
        print('Available commands:')
        print('  v_schema <schema> - Validate a JADN Schema')
        print('  v_data <data> <schema> - Validate Data against a JADN Schema')
        print('  c_schema <schema> <convert_to> - Convert JADN Schema to another format, such as <json> or <xsd>')
        print('  c_data <data> <schema> <convert_to> - Convert a data to another format, such as <json>, <cbor> or <xml>')
        print('  vis_schema <schema> <vis_to> - Visualize the JADN Schema in another format such as <plantuml>, <graphviz>, <md> or <jidl>.')
        print('  clear - Clear the screen.')
        print('  version - Print the JADN CLI Version.')
        print('  exit - Exit the JADN CLI.')
        
    def do_version(self, arg):
        'Show the version of the JADN CLI.'
        print('JADN CLI version 1.0.0')
        
    def do_list(self, arg):
        'List all available commands.'
        print('Available commands:')
        print('  v_schema')
        print('  v_data')
        print('  c_schema')
        print('  c_data')
        print('  vis_schema')
        print('  clear')
        print('  exit')
        print('  help')
        print('  version')
        
if __name__ == '__main__':
    JadnCLI().cmdloop()        