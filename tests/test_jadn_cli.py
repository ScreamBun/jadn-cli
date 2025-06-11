import cmd
import sys
from jadn_cli import JadnCLI


def test_do_v_schema():
    arg = "music-database.jadn"
    
    cli = JadnCLI()
    cli.do_schema_v(arg)
    cli.do_err_report_gen('')
    
    assert cli.error_list == [] 
    
def test_do_v_data():
    arg = "music-database.jadn music_library.json"
    
    cli = JadnCLI()
    cli.do_data_v(arg)
    cli.do_err_report_gen('')
    
    assert cli.error_list == []     
    
def test_do_help(): 
    arg = ""
    
    version_info = sys.version_info
    version_string = sys.version
    a = sys.prefix
    b = sys.base_prefix
    
    cli = JadnCLI()
    cli.do_help(arg)
    
    assert cli.error_list == []