import marshmallow as mm
import pytest
from emannotationschemas.models import (
    Base,
    InvalidSchemaField,
    make_sqlalchemy_model,
    make_model_from_schema,
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
        include_contacts=True,
        segmentation_source=None,
        metadata_dict=metadata_dict,
        with_crud_columns=True
    )
    check_model_dict(model_dict, "synapse", "synapse")
    check_model_dict(model_dict, "contact", "test__contact")
    check_model_dict(model_dict, "spinecall", "spinecall")


def check_model_dict(model_dict, schema_type, table_name):
    synapse_model = model_dict[schema_type]
    assert synapse_model.__name__ == table_name
    assert issubclass(synapse_model, Base)


def test_wrong_reference_schmea():
    """Check that non-reference schema skips
    reference schema columns during model creation when
    optional metadata dict is passed with a reference"""
    table_args = {
        "table_name": "bad_reference_table",
        "schema_type": "synapse",
        "segmentation_source": None,
        "table_metadata": {"reference_table": "anno_table"},
        "with_crud_columns": True
    }
    
    ref_anno_model = make_sqlalchemy_model(**table_args)
    assert not hasattr(ref_anno_model, "target_id")


def test_model_failure():
    class NestSchema(mm.Schema):
        a = mm.fields.Email()

    class BadSchema(mm.Schema):
        nest = mm.fields.Nested(NestSchema, many=True)

    with pytest.raises(InvalidSchemaField):
        make_model_from_schema("testBad", BadSchema)
    with pytest.raises(InvalidSchemaField):
        make_model_from_schema("testNest", NestSchema)
