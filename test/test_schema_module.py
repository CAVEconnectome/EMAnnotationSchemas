from emannotationschemas import get_schema, get_types
from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas.base import AnnotationSchema
import pytest


def test_get_types():
    types = get_types()
    for type_ in types:
        schema = get_schema(type_)
        assert issubclass(schema, AnnotationSchema)


def test_bad_type():
    with pytest.raises(UnknownAnnotationTypeException):
        get_schema('NOTAVALIDTYPE')
