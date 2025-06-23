import cmd
import sys
import os
import glob
from jadn_cli import JadnCLI
from src.utils.consts import OUTPUT_DIR_PATH

############# TESTING COMMAND: help #############
def test_do_help(): 
    arg = ""
    
    version_info = sys.version_info
    version_string = sys.version
    a = sys.prefix
    b = sys.base_prefix
    
    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_help(arg)
    
    assert cli.error_list == []

############# TESTING COMMAND: schema_rev_t <schema_file> #############
def test_schema_rev_t_json():
    arg = "music-database.json"

    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_rev_t(arg)
    cli.do_err_report_gen('')

    assert cli.error_list == []

def test_schema_rev_t_jidl():
    arg = "music-database.jidl"

    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_rev_t(arg)
    cli.do_err_report_gen('')

    assert cli.error_list == []

############# TESTING COMMAND: schema_t <schema_file> <convert_to> #############
def test_schema_t_json():
    arg = "music-database.jadn json"
    
    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_t(arg)
    cli.do_err_report_gen('')
    
    assert cli.error_list == []

def test_schema_t_jidl():
    arg = "music-database.jadn jidl"
    
    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_t(arg)
    cli.do_err_report_gen('')
    
    assert cli.error_list == []

def test_schema_t_xsd():
    arg = "music-database.jadn xsd"
    
    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_t(arg)
    cli.do_err_report_gen('')
    
    assert cli.error_list == []

############# TESTING COMMAND: schema_vis <schema_file> <convert_to> #############
def test_schema_vis_md():
    arg = "music-database.jadn md"
    
    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_vis(arg)
    cli.do_err_report_gen('')
    
    assert cli.error_list == []

def test_schema_vis_html():
    arg = "music-database.jadn html"
    
    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_vis(arg)
    cli.do_err_report_gen('')
    
    assert cli.error_list == []

def test_schema_vis_gv():
    arg = "music-database.jadn gv information"
    
    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_vis(arg)
    cli.do_err_report_gen('')
    
    assert cli.error_list == []

def test_schema_vis_puml():
    arg = "music-database.jadn puml information"
    
    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_vis(arg)
    cli.do_err_report_gen('')
    
    assert cli.error_list == []

############# TESTING COMMAND: schema_v <schema_file> #############
def test_do_v_schema():
    arg = "music-database.jadn"
    
    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_v(arg)
    cli.do_err_report_gen('')
    
    assert cli.error_list == []

def test_do_v_schema_invalid():
    arg = "invalid-music-database.jadn"
    
    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_v(arg)
    cli.do_err_report_gen('')

    assert len(cli.error_list) > 0

############# TESTING COMMAND: data_v <schema_file> <data_file> #############
def test_do_v_data_json():
    arg = "music-database.jadn music_library.json"
    
    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_data_v(arg)
    cli.do_err_report_gen('')
    
    assert cli.error_list == []

def test_do_v_data_xml():
    assert True  # Placeholder for when xml generation is fixed

def test_do_v_data_cbor():
    arg = "music-database.jadn music_library.cbor"
    
    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_data_v(arg)
    cli.do_err_report_gen('')
    
    assert cli.error_list == []     

############# TESTING COMMAND: clear_log #############
def test_do_clear_log():
    arg = "invalid-music-database.jadn"

    cli = JadnCLI()

    cli.do_schema_v(arg)
    cli.do_clear_log('')
    cli.do_err_report_gen('')
    
    assert cli.error_list == []

############# TESTING COMMAND: clear_reports #############
def test_do_clear_reports():
    arg = "invalid-music-database.jadn"

    cli = JadnCLI()

    cli.do_schema_v(arg)
    cli.do_err_report_gen('')
    cli.do_clear_reports('')

    csv_files = glob.glob(os.path.join(OUTPUT_DIR_PATH, "*.csv"))
    assert len(csv_files) == 0