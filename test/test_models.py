from emannotationschemas.models import make_all_models, InvalidSchemaField
from emannotationschemas.models import make_annotation_model_from_schema
from sqlalchemy.ext.declarative import AbstractConcreteBase
import pytest
import marshmallow as mm


def test_model_creation():
    model_dict = make_all_models(['test'])
    model = model_dict['test']['synapse']
    assert(model.__name__ == "TestSynapse")
    assert(issubclass(model, AbstractConcreteBase))
    # TODO better tests here


def test_model_failure():
    class NestSchema(mm.Schema):
        a = mm.fields.Email()

    class BadSchema(mm.Schema):
        nest = mm.fields.Nested(NestSchema, many=True)

    with pytest.raises(InvalidSchemaField):
        make_annotation_model_from_schema('test', 'badschema', BadSchema)
    with pytest.raises(InvalidSchemaField):
        make_annotation_model_from_schema('test', 'nestschema', NestSchema)
