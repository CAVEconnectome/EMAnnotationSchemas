import marshmallow as mm
import pytest

from emannotationschemas import get_schema, get_types
from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas.flatten import create_flattened_schema
from emannotationschemas.schemas.base import AnnotationSchema, SpatialPoint
from emannotationschemas.schemas.nucleus_detection import NucleusDetection


def test_get_types():
    types = get_types()
    for type_ in types:
        schema = get_schema(type_)
        assert issubclass(schema, AnnotationSchema) or issubclass(schema, SpatialPoint)


def test_bad_type():
    with pytest.raises(UnknownAnnotationTypeException):
        get_schema("NOTAVALIDTYPE")


def test_flattened_schema_nulls():
    """Test that flattened schemas preserve required=False on nested fields"""
    
    FlatSchema = create_flattened_schema(NucleusDetection)
    flat_schema = FlatSchema()
    
    assert flat_schema.fields['pt_position'].required == True
    
    assert flat_schema.fields['bb_start_position'].required == False
    assert flat_schema.fields['bb_end_position'].required == False

    for field_name, field in flat_schema.fields.items():
        print(f"{field_name}: required={field.required}")


def test_nested_field_required_preservation():
    """Test that flattened schemas preserve required=False on nested fields"""
    
    class TestSchema(AnnotationSchema):
        required_point = mm.fields.Nested(
            SpatialPoint,
            required=True,
            description="A required spatial point"
        )
        optional_point = mm.fields.Nested(
            SpatialPoint,
            required=False,
            description="An optional spatial point"
        )
    
    FlatSchema = create_flattened_schema(TestSchema)
    flat_schema = FlatSchema()
    
    assert flat_schema.fields['required_point_position'].required == True
    
    assert flat_schema.fields['optional_point_position'].required == False
    
    assert flat_schema.fields['optional_point_position'].allow_none == True
    
    data = {
        'required_point_position': [1, 2, 3],
    }
    try:
        result = flat_schema.load(data)
        assert result['optional_point_position'] is None
    except mm.ValidationError as e:
        pytest.fail(f"Validation failed for optional nested fields: {e}")
    
    data = {
        'optional_point_position': [1, 2, 3],
    }
    with pytest.raises(mm.ValidationError):
        flat_schema.load(data)