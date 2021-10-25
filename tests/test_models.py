import marshmallow as mm
import pytest
from emannotationschemas.models import (
    Base,
    InvalidSchemaField,
    make_annotation_model_from_schema,
    make_dataset_models,
)

def test_model_creation():
    metadata_dict = {"spinecall": {"reference_table": "synapse"}}
    model_dict = make_dataset_models(
        aligned_volume="test",
        schemas_and_tables=[("synapse", "synapse"), ("postsynaptic_compartment", "spinecall")],
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
    # TODO better tests here


def test_model_failure():
    class NestSchema(mm.Schema):
        a = mm.fields.Email()

    class BadSchema(mm.Schema):
        nest = mm.fields.Nested(NestSchema, many=True)

    with pytest.raises(InvalidSchemaField):
        make_annotation_model_from_schema("testBad", BadSchema)
    with pytest.raises(InvalidSchemaField):
        make_annotation_model_from_schema("testNest", NestSchema)
