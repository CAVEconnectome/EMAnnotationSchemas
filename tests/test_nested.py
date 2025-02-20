import marshmallow as mm
import logging
from emannotationschemas import get_types, get_schema
from emannotationschemas.flatten import create_flattened_schema

def find_nested_fields(schema):
    """Find all nested fields in a schema and their required status
    
    Parameters
    ----------
    schema : marshmallow.Schema
        The schema to inspect
        
    Returns
    -------
    dict
        Dictionary mapping nested field paths to their required status
    """
    nested_fields = {}
    
    for field_name, field in schema._declared_fields.items():
        if isinstance(field, mm.fields.Nested):
            nested_fields[field_name] = {
                'required': field.required,
                'subfields': find_nested_fields(field.nested)
            }
    
    return nested_fields

def test_all_schemas_preserve_required():
    """Test that flattening preserves required=False for all nested fields across all schemas"""
    
    schema_types = get_types()
    
    for schema_type in schema_types:
        logging.info(f"\nTesting schema: {schema_type}")
        Schema = get_schema(schema_type)
        
        nested_fields = find_nested_fields(Schema)
        
        FlatSchema = create_flattened_schema(Schema)
        flat_schema = FlatSchema()
        
        for nested_name, nested_info in nested_fields.items():
            if not nested_info['required']:
                for field_name, field in flat_schema.fields.items():
                    if field_name.startswith(f"{nested_name}_"):
                        logging.info(f"  Checking {field_name} (from optional nested field {nested_name})")
                        assert field.required == False, \
                            f"Schema {schema_type}: Field {field_name} should not be required because parent {nested_name} was not required"