from emannotationschemas.models import make_all_models, InvalidSchemaField
from emannotationschemas.models import make_annotation_model_from_schema
from sqlalchemy.ext.declarative import AbstractConcreteBase
import pytest
import marshmallow as mm


def test_model_creation():
    model_dict = make_all_models(['test', 'test2'], include_contacts=True)
    model = model_dict['test']['synapse']
    assert(model.__name__ == "TestSynapse")
    model = model_dict['test2']['synapse']
    assert(model.__name__ == "Test2Synapse")
    model = model_dict['test']['cellsegment']
    assert(model.__name__ == "TestCellSegment")
    model = model_dict['test']['contact']
    assert(model.__name__ == "TestContact")

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
