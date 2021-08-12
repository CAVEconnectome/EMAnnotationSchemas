import pytest
from emannotationschemas import get_schema, get_types
from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas.schemas.base import AnnotationSchema, SpatialPoint


def test_get_types():
    types = get_types()
    for type_ in types:
        schema = get_schema(type_)
        assert issubclass(schema, AnnotationSchema) or issubclass(schema, SpatialPoint)


def test_bad_type():
    with pytest.raises(UnknownAnnotationTypeException):
        get_schema("NOTAVALIDTYPE")
