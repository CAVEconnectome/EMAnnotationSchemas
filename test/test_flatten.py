from emannotationschemas import get_flat_schema, get_types
from emannotationschemas.errors import UnknownAnnotationTypeException
import pytest


def test_flatten_all():
    types = get_types()
    for type_ in types:
        Schema = get_flat_schema(type_)


def test_bad_flatten():
    with pytest.raises(UnknownAnnotationTypeException):
        get_flat_schema('NOT A REAL TYPE')
