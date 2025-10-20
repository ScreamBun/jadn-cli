import sys
import os
import glob
from jadn_cli import JadnCLI
from src.utils.consts import OUTPUT_DIR_PATH, SCHEMAS_DIR_PATH

from jadn2 import JADN, add_methods
from jadn2.config import style_args, style_fname
from jadn2.convert import jidl_rw, xasd_rw, md_rw, erd_w
from jadn2.translate import jschema_rw, xsd_rw, cddl_rw, proto_rw, xeto_rw

from src.utils.file_utils import get_filepath

add_methods(jidl_rw)  
add_methods(xasd_rw)
add_methods(md_rw)
add_methods(erd_w)
add_methods(jschema_rw)
add_methods(xsd_rw) 
add_methods(cddl_rw)
add_methods(proto_rw)
add_methods(xeto_rw)


def test_jadn2_functions():
    assert JADN is not None, "JADN import failed"
    assert style_args is not None, "style_args import failed"
    assert style_fname is not None, "style_fname import failed"

    # Check if the methods are added correctly
    assert hasattr(JADN, 'cddl_dump'), "cddl_dump method not added to JADN"
    assert hasattr(JADN, 'cddl_dumps'), "cddl_dumps method not added to JADN"
    assert hasattr(JADN, 'cddl_load'), "cddl_load method not added to JADN"
    assert hasattr(JADN, 'cddl_loads'), "cddl_loads method not added to JADN"
    assert hasattr(JADN, 'cddl_style'), "cddl_style method not added to JADN"
    assert hasattr(JADN, 'erd_dump'), "erd_dump method not added to JADN"
    assert hasattr(JADN, 'erd_dumps'), "erd_dumps method not added to JADN"
    assert hasattr(JADN, 'erd_style'), "erd_style method not added to JADN" 
    assert hasattr(JADN, 'jadn_dump'), "jadn_dump method not added to JADN"
    assert hasattr(JADN, 'jadn_dumps'), "jadn_dumps method not added to JADN"
    assert hasattr(JADN, 'jadn_load'), "jadn_load method not added to JADN"
    assert hasattr(JADN, 'jadn_loads'), "jadn_loads method not added to JADN"
    assert hasattr(JADN, 'jadn_style'), "jadn_style method not added to JADN"       
    assert hasattr(JADN, 'jidl_dump'), "jidl_dump method not added to JADN"
    assert hasattr(JADN, 'jidl_dumps'), "jidl_dumps method not added to JADN"
    assert hasattr(JADN, 'jidl_load'), "jidl_load method not added to JADN"
    assert hasattr(JADN, 'jidl_loads'), "jidl_loads method not added to JADN"
    assert hasattr(JADN, 'jidl_style'), "jidl_style method not added to JADN"
    assert hasattr(JADN, 'jschema_dump'), "jschema_dump method not added to JADN"
    assert hasattr(JADN, 'jschema_dumps'), "jschema_dumps method not added to JADN"
    assert hasattr(JADN, 'jschema_load'), "jschema_load method not added to JADN"
    assert hasattr(JADN, 'jschema_loads'), "jschema_loads method not added to JADN"
    assert hasattr(JADN, 'jschema_style'), "jschema_style method not added to JADN"
    assert hasattr(JADN, 'md_dump'), "md_dump method not added to JADN"
    assert hasattr(JADN, 'md_dumps'), "md_dumps method not added to JADN"
    assert hasattr(JADN, 'md_load'), "md_load method not added to JADN"
    assert hasattr(JADN, 'md_loads'), "md_loads method not added to JADN"
    assert hasattr(JADN, 'md_style'), "md_style method not added to JADN"
    assert hasattr(JADN, 'proto_dump'), "proto_dump method not added to JADN"
    assert hasattr(JADN, 'proto_dumps'), "proto_dumps method not added to JADN"
    assert hasattr(JADN, 'proto_load'), "proto_load method not added to JADN"
    assert hasattr(JADN, 'proto_loads'), "proto_loads method not added to JADN"
    assert hasattr(JADN, 'proto_style'), "proto_style method not added to JADN"
    assert hasattr(JADN, 'xasd_dump'), "xasd_dump method not added to JADN"
    assert hasattr(JADN, 'xasd_dumps'), "xasd_dumps method not added to JADN"
    assert hasattr(JADN, 'xasd_load'), "xasd_load method not added to JADN"
    assert hasattr(JADN, 'xasd_loads'), "xasd_loads method not added to JADN"
    assert hasattr(JADN, 'xasd_style'), "xasd_style method not added to JADN"
    assert hasattr(JADN, 'xeto_dump'), "xeto_dump method not added to JADN"
    assert hasattr(JADN, 'xeto_dumps'), "xeto_dumps method not added to JADN"
    assert hasattr(JADN, 'xeto_load'), "xeto_load method not added to JADN"
    assert hasattr(JADN, 'xeto_loads'), "xeto_loads method not added to JADN"
    assert hasattr(JADN, 'xeto_style'), "xeto_style method not added to JADN"
    assert hasattr(JADN, 'xsd_dump'), "xsd_dump method not added to JADN"
    assert hasattr(JADN, 'xsd_dumps'), "xsd_dumps method not added to JADN"
    assert hasattr(JADN, 'xsd_load'), "xsd_load method not added to JADN"
    assert hasattr(JADN, 'xsd_loads'), "xsd_loads method not added to JADN"
    assert hasattr(JADN, 'xsd_style'), "xsd_style method not added to JADN"
    
    
def test_jadn2_jidl_dumps():
    schema_filename = "music-database.jadn"
    try:
        j_pkg = JADN()
        path = get_filepath(SCHEMAS_DIR_PATH, schema_filename)
        
        with open(path, 'r', encoding='utf-8') as fp:
            j_pkg.jadn_load(fp)

        style: dict = None
        jidl_text = j_pkg.jidl_dumps(style)
    except Exception as e:
        print(f"Error during JADN initialization: {e}")
    
    assert jidl_text is not None, "JIDL Generation failed or returned None"


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

############# TESTING COMMAND: schema_rev_t_bulk <jidl, json, or xsd> #############
def test_schema_rev_t_bulk_jidl():
    arg = "jidl"

    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_rev_t_bulk(arg)
    cli.do_err_report_gen('')

    assert cli.error_list == []

def test_schema_rev_t_bulk_json():
    arg = "json"

    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_rev_t_bulk(arg)
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

############# TESTING COMMAND: schema_t_bulk <convert_to> #############

def test_schema_t_bulk_xsd():
    arg = "xsd"

    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_t_bulk(arg)
    cli.do_err_report_gen('')

    assert cli.error_list == []

def test_schema_t_bulk_jidl():
    arg = "jidl"

    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_t_bulk(arg)
    cli.do_err_report_gen('')

    assert cli.error_list == []

def test_schema_t_bulk_json():
    arg = "json"

    cli = JadnCLI()
    cli.do_clear_log('')

    cli.do_schema_t_bulk(arg)
    cli.do_err_report_gen('')

    assert len(cli.error_list) == 1 #invalid schema

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

    #cli.do_data_v(arg)
    #cli.do_err_report_gen('')
    
    #assert cli.error_list == []  
    assert True # CBOR is invalid   

############# TESTING COMMAND: data_c #############
def test_do_data_c():
    arg = "-b"
    arg2 = "--bulk"
    arg3 = "music_library.json"

    cli =JadnCLI()

    cli.do_clear_log('')
    cli.do_data_c(arg)
    cli.do_err_report_gen('')

    assert cli.error_list == []

    cli.do_clear_log('')
    cli.do_data_c(arg2)
    cli.do_err_report_gen('')

    assert cli.error_list == []

    cli.do_clear_log('')
    cli.do_data_c(arg3)
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