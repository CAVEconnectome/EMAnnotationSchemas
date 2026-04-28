import pytest
from marshmallow import ValidationError
from sqlalchemy import BigInteger

from emannotationschemas.models import make_model_from_schema
from emannotationschemas.schemas.base import (
    AnnotationSchema,
    AutoUserIdField,
    BoundSpatialPoint,
)
from emannotationschemas.flatten import create_flattened_schema
import marshmallow as mm


class _UserSchema(AnnotationSchema):
    """Minimal schema with an AutoUserIdField for testing."""
    pt = mm.fields.Nested(BoundSpatialPoint, required=True)
    user_id = AutoUserIdField(required=True, description="test auto user id")


def annotation_import(item):
    item["supervoxel_id"] = None
    item.pop("rootId", None)


good_data = {"pt": {"position": [1, 2, 3]}, "user_id": 42}
missing_user_id = {"pt": {"position": [1, 2, 3]}}


def test_auto_user_id_field_is_int_subclass():
    assert issubclass(AutoUserIdField, mm.fields.Int)


def test_auto_user_id_field_detected_by_isinstance():
    schema = _UserSchema()
    flat = create_flattened_schema(_UserSchema)
    auto_fields = [
        name
        for name, field in flat._declared_fields.items()
        if isinstance(field, AutoUserIdField)
    ]
    assert auto_fields == ["user_id"]


def test_schema_loads_with_user_id():
    schema = _UserSchema(context={"bsp_fn": annotation_import})
    result = schema.load(good_data)
    assert result["user_id"] == 42


def test_schema_rejects_missing_user_id():
    schema = _UserSchema(context={"bsp_fn": annotation_import})
    with pytest.raises(ValidationError):
        schema.load(missing_user_id)


def test_model_creation_with_auto_user_id_field():
    model = make_model_from_schema("test_auto_user_id_table", "bound_tag_user", reset_cache=True)
    col_names = [col.name for col in model.__table__.columns]
    assert "user_id" in col_names


def test_auto_user_id_column_is_biginteger():
    model = make_model_from_schema("test_auto_user_id_col_type", "bound_tag_user", reset_cache=True)
    user_id_col = next(col for col in model.__table__.columns if col.name == "user_id")
    assert isinstance(user_id_col.type, BigInteger)


def test_bound_tag_user_model_creation():
    """Verify a real *User schema creates its model without error."""
    model = make_model_from_schema(
        "test_bound_tag_user_model", "bound_tag_user", reset_cache=True
    )
    col_names = [col.name for col in model.__table__.columns]
    assert "user_id" in col_names


def test_proofreading_bool_status_user_model_creation():
    """Verify ProofreadingBoolStatusUser creates its model without error."""
    model = make_model_from_schema(
        "test_proofreading_user_model", "proofreading_boolstatus_user", reset_cache=True
    )
    col_names = [col.name for col in model.__table__.columns]
    assert "user_id" in col_names
