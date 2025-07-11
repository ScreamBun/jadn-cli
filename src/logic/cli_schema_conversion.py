import json
import jadn

from jadnschema.convert import dumps
from jadnxml.builder.xsd_builder import convert_xsd_from_dict
from src.utils.consts import CSS_DIR_PATH, GV_FILE_EXT, HTML_FILE_EXT, JIDL_FILE_EXT, JSON_FILE_EXT, MARKDOWN_FILE_EXT, PLANT_UML_FILE_EXT, SCHEMA_CSS_FILE_NAME, SCHEMAS_DIR_PATH, XSD_FILE_EXT
from src.utils.file_utils import get_file, get_filepath

class CliSchemaConversion():
    
    schema_filename: str = None
    convert_to: str = None
    errors: list = []
    
    def __init__(self, schema_filename: str, convert_to: str = None):
        self.schema_filename = schema_filename
        self.convert_to = convert_to

    def convert(self, opt = 'information'):
        converted_schema = None
        
        schema_file_data = get_file(SCHEMAS_DIR_PATH, self.schema_filename)
        if not schema_file_data:
            raise ValueError(f"jadn schema {self.schema_filename} not found.  Double check the schema folder and filename.")
        
        try:
            schema_data_str = schema_file_data[self.schema_filename]
            schema_data = json.loads(schema_data_str) # Ensure it's a valid JSON string
            
            if self.convert_to == GV_FILE_EXT:
                gv_style = jadn.convert.diagram_style()
                gv_style['format'] = 'graphviz'
                gv_style['detail'] = opt
                gv_style['attributes'] = True
                gv_style['enums'] = 100
                
                converted_schema = jadn.convert.diagram_dumps(schema_data, gv_style)
            
            elif self.convert_to == HTML_FILE_EXT:
                kwargs = { "fmt": self.convert_to }
                kwargs["styles"] = get_filepath(CSS_DIR_PATH, SCHEMA_CSS_FILE_NAME)
                converted_schema = dumps(schema_data, **kwargs)
            
                # TODO: Does JADN not have an html converter?
                # html_style = jadn.convert.html5()
                # converted_schema = jadn.convert.html5_dumps(schema_data, html_style)        
            
            elif self.convert_to == JSON_FILE_EXT:
                converted_schema = jadn.translate.json_schema_dumps(schema_data)
            
            elif self.convert_to == JIDL_FILE_EXT:
                jidl_style = jadn.convert.jidl_style()
                converted_schema = jadn.convert.jidl_dumps(schema_data, jidl_style)
                
            elif self.convert_to == MARKDOWN_FILE_EXT:
                converted_schema = jadn.convert.markdown_dumps(schema_data)
                
            elif self.convert_to == PLANT_UML_FILE_EXT:
                puml_style = jadn.convert.diagram_style()
                puml_style['format'] = 'plantuml'
                puml_style['detail'] = opt
                puml_style['attributes'] = True
                puml_style['enums'] = 100
                converted_schema = jadn.convert.diagram_dumps(schema_data, puml_style)
                
            elif self.convert_to == XSD_FILE_EXT:
                result = convert_xsd_from_dict(schema_data)
                if result and isinstance(result, tuple):
                    converted_schema = result[0]
                
        except Exception as e:
            raise ValueError(f"Schema Invalid - {e}")
        
        return converted_schema