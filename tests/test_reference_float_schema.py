import pytest
from marshmallow import ValidationError

from emannotationschemas import get_schema, get_types
from emannotationschemas.schemas.reference_float import (
    ReferenceDoubleFloat,
    ReferenceTripleFloat,
)

target_id = 1


def test_reference_double_float():
    result = ReferenceDoubleFloat().load(
        {"target_id": target_id, "value": 0.5, "value2": 1.5}
    )
    assert result["target_id"] == target_id
    assert result["value"] == 0.5
    assert result["value2"] == 1.5


def test_reference_triple_float():
    result = ReferenceTripleFloat().load(
        {"target_id": target_id, "value": 0.1, "value2": 0.2, "value3": 0.3}
    )
    assert result["value"] == 0.1
    assert result["value2"] == 0.2
    assert result["value3"] == 0.3


def test_reference_double_float_missing_value():
    with pytest.raises(ValidationError):
        ReferenceDoubleFloat().load({"target_id": target_id, "value": 0.5})


def test_registered_in_type_mapping():
    assert get_schema("reference_double_float") is ReferenceDoubleFloat
    assert get_schema("reference_triple_float") is ReferenceTripleFloat
    assert "reference_double_float" in get_types()
    assert "reference_triple_float" in get_types()
