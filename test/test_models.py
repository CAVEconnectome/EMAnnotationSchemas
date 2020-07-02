from emannotationschemas.models import make_dataset_models, InvalidSchemaField
from emannotationschemas.models import make_annotation_model_from_schema
from emannotationschemas.models import Base
import pytest
import marshmallow as mm


def test_model_creation():
    metadata_dict = {
                        'spinecall':{
                            'reference_table':'synapse'
                        }
                    }
    model_dict = make_dataset_models('test', [('synapse', 'synapse'),
                                              ('postsynaptic_compartment', 'spinecall')],
                                              include_contacts=True)
    model = model_dict['synapse']
    assert(model.__name__ == "TestSynapse")
    model = model_dict['cellsegment']
    assert(model.__name__ == "TestCellSegment")
    model = model_dict['contact']
    assert(model.__name__ == "TestContact")
    model = model_dict['spinecall']
    assert(model.__name__ == 'TestSynapseflatref')
    assert(issubclass(model, Base))

    # TODO better tests here


def test_model_failure():
    class NestSchema(mm.Schema):
        a = mm.fields.Email()

    class BadSchema(mm.Schema):
        nest = mm.fields.Nested(NestSchema, many=True)

    with pytest.raises(InvalidSchemaField):
        make_annotation_model_from_schema('test',BadSchema)
    with pytest.raises(InvalidSchemaField):
        make_annotation_model_from_schema('test', NestSchema)
