import marshmallow as mm
import pytest
from emannotationschemas.models import (
    Base,
    InvalidSchemaField,
    make_annotation_model,
    make_annotation_model_from_schema,
    make_dataset_models,
)


def test_model_creation():
    metadata_dict = {"spinecall": {"reference_table": "synapse"}}
    model_dict = make_dataset_models(
        aligned_volume="test",
        schemas_and_tables=[
            ("synapse", "synapse"),
            ("postsynaptic_compartment", "spinecall"),
        ],
        metadata_dict=metadata_dict,
        include_contacts=True,
    )
    synapse_model = model_dict["synapse"]
    assert synapse_model.__name__ == "synapse"
    assert issubclass(synapse_model, Base)

    contact_model = model_dict["contact"]
    assert contact_model.__name__ == "test__contact"
    assert issubclass(contact_model, Base)

    ref_model = model_dict["spinecall"]
    assert ref_model.__name__ == "spinecall"
    assert issubclass(ref_model, Base)


def test_wrong_reference_schmea():
    """Check that non-reference schema skips
    reference schema columns during model creation when
    optional metadata dict is passed with a reference"""
    table_name = "bad_reference_table"
    schema_type = "synapse"
    table_metadata = {"reference_table": "anno_table"}
    ref_anno_model = make_annotation_model(table_name, schema_type, table_metadata)
    assert not hasattr(ref_anno_model, "target_id")


def test_model_failure():
    class NestSchema(mm.Schema):
        a = mm.fields.Email()

    class BadSchema(mm.Schema):
        nest = mm.fields.Nested(NestSchema, many=True)

    with pytest.raises(InvalidSchemaField):
        make_annotation_model_from_schema("testBad", BadSchema)
    with pytest.raises(InvalidSchemaField):
        make_annotation_model_from_schema("testNest", NestSchema)
