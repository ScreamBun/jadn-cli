import cmd

class JadnCLI(cmd.Cmd):
    intro = 'Welcome to the JSON Abstract Data Notation (JADN) CLI tool. Type help or ? to list commands.\n'
    prompt = '(jadn) '

    def do_exit(self, arg):
        'Exit the JADN CLI.'
        print('See you next time. ')
        return True
        
    def do_add(self, arg):
        'Add two numbers. Usage: add <num1> <num2>'
        try:
            num1, num2 = map(int, arg.split())
            print(f'The sum is: {num1 + num2}')
        except ValueError:
            print('Invalid input. Please provide two numbers.')
            
    def do_subtract(self, arg):
        'Subtract two numbers. Usage: subtract <num1> <num2>'
        try:
            num1, num2 = map(int, arg.split())
            print(f'The difference is: {num1 - num2}')
        except ValueError:
            print('Invalid input. Please provide two numbers.')
            
    def do_multiply(self, arg):
        'Multiply two numbers. Usage: multiply <num1> <num2>'
        try:
            num1, num2 = map(int, arg.split())
            print(f'The product is: {num1 * num2}')
        except ValueError:
            print('Invalid input. Please provide two numbers.')
            
    def do_divide(self, arg):
        'Divide two numbers. Usage: divide <num1> <num2>'
        try:
            num1, num2 = map(int, arg.split())
            if num2 == 0:
                print('Error: Division by zero.')
            else:
                print(f'The quotient is: {num1 / num2}')
        except ValueError:
            print('Invalid input. Please provide two numbers.')
            
    def do_clear(self, arg):
        'Clear the screen.'
        print('\033c', end='')
        
    def do_help(self, arg):
        'List available commands.'
        print('Available commands:')
        print('  add <num1> <num2>  - Add two numbers.')
        print('  subtract <num1> <num2> - Subtract two numbers.')
        print('  multiply <num1> <num2> - Multiply two numbers.')
        print('  divide <num1> <num2>   - Divide two numbers.')
        print('  clear              - Clear the screen.')
        print('  exit               - Exit the JADN CLI.')
        
    def do_version(self, arg):
        'Show the version of the JADN CLI.'
        print('JADN CLI version 1.0.0')
        
    def do_list(self, arg):
        'List all available commands.'
        print('Available commands:')
        print('  hello')
        print('  add')
        print('  subtract')
        print('  multiply')
        print('  divide')
        print('  clear')
        print('  exit')
        print('  help')
        print('  version')
        
if __name__ == '__main__':
    JadnCLI().cmdloop()        