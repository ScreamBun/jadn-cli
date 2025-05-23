from jadn_cli import JadnCLI


def test_do_v_schema():
    arg = "music-database.jadn"
    
    cli = JadnCLI()
    cli.do_v_schema(arg)
    cli.do_gen_err_report('')
    
    assert cli.error_list == [] 
    
def test_do_help():
    arg = ""
    
    cli = JadnCLI()
    cli.do_help(arg)
    
    assert cli.error_list == []     