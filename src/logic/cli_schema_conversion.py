import json
import jadn

from jadnxml.builder.xsd_builder import XSDBuilder
from jadnutils.html.html_converter import HtmlConverter
from src.utils.consts import GV_FILE_EXT, HTML_FILE_EXT, JIDL_FILE_EXT, JSON_FILE_EXT, MARKDOWN_FILE_EXT, PLANT_UML_FILE_EXT, SCHEMAS_DIR_PATH, XSD_FILE_EXT
from src.utils.file_utils import get_file

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
            
            # Validate and fix schema structure before conversion
            self._validate_and_fix_schema(schema_data)
            
            if self.convert_to == GV_FILE_EXT:
                gv_style = jadn.convert.diagram_style()
                gv_style['format'] = 'graphviz'
                gv_style['detail'] = opt
                gv_style['attributes'] = True
                gv_style['enums'] = 100
                
                converted_schema = jadn.convert.diagram_dumps(schema_data, gv_style)
            
            elif self.convert_to == HTML_FILE_EXT:
                converter = HtmlConverter(schema_data)
                converted_schema = converter.jadn_to_html(run_validation=False)    
            
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
                xsd_builder = XSDBuilder()
                result = xsd_builder.convert_xsd_from_dict(schema_data)
                if result and isinstance(result, tuple):
                    converted_schema = result[0]
                
        except Exception as e:
            raise ValueError(f"Schema Invalid - {e}")
        
        return converted_schema
    
    def _validate_and_fix_schema(self, schema_data):
        """
        Validate and fix common schema structure issues that can cause conversion errors.
        """
        if not isinstance(schema_data, dict) or 'types' not in schema_data:
            raise ValueError("Schema must be a dictionary with a 'types' key")
        
        types = schema_data.get('types', [])
        if not isinstance(types, list):
            raise ValueError("Schema 'types' must be a list")
        
        # Fix type definitions that are missing the Fields array (index 4)
        for i, type_def in enumerate(types):
            if not isinstance(type_def, list):
                raise ValueError(f"Type definition {i} must be a list")
            
            # Each type definition should have at least 5 elements:
            # [name, base_type, options, description, fields]
            if len(type_def) < 5:
                # Add missing elements with appropriate defaults
                while len(type_def) < 4:
                    type_def.append('')  # Add empty description if missing
                type_def.append([])  # Add empty fields array
                
                print(f"Warning: Fixed malformed type definition '{type_def[0] if len(type_def) > 0 else 'Unknown'}' - added missing fields array")
        
        return schema_data