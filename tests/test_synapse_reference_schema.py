import pytest
from emannotationschemas.schemas.synapse import SynapseSchema
from emannotationschemas.schemas.presynaptic_bouton_type import PresynapticBoutonType
from emannotationschemas.schemas.postsynaptic_compartment import PostsynapticCompartment

from emannotationschemas.flatten import flatten_dict
from emannotationschemas import get_flat_schema
from marshmallow import ValidationError

synapse_id = 1

good_bouton = {
    'bouton_type': 'basmati',
    'target_id': synapse_id
    }

bad_bouton = {
    'bouton_type': 'some_nonsense',
    'target_id': synapse_id
    }

good_compartment = {
    'compartment': 'soma',
    'target_id': synapse_id
    }

rich_compartment = {
    'compartment': 'dendrite',
    'on_spine' : True,
    'dendrite_class' : 'apical',
    'target_id': synapse_id
    }

bad_compartment = {
    'compartment': 'some_nonsense',
    'target_id': synapse_id
    }

def test_bad_bouton_type():
    with pytest.raises(Exception):
        assert check_bad_bouton_type()

def test_good_bouton_type():
    with pytest.raises(Exception):
        assert check_good_bouton_type()


def check_bad_bouton_type():
    schema = PresynapticBoutonType()
    try:
        result = schema.load(bad_bouton)
    except ValidationError as err:
        raise Exception(f"Wrong type {err}")


def check_good_bouton_type():
    schema = PresynapticBoutonType()
    try:
        result = schema.load(good_bouton)
    except ValidationError as err:
        raise Exception(f"Wrong type {err}")


def test_good_postsynaptic_compartment():
    with pytest.raises(Exception):
        assert check_good_postsynaptic_compartment()


def test_bad_postsynaptic_compartment():
    with pytest.raises(Exception):
        assert check_bad_postsynaptic_compartment()


def test_rich_postsynaptic_compartment():
    with pytest.raises(Exception):
        assert check_rich_postsynaptic_compartment()


def check_good_postsynaptic_compartment():
    schema = PostsynapticCompartment()
    try:
        result = schema.load(good_compartment)
        assert( result['compartment'] == 'soma' )
    except ValidationError as err:
        raise Exception(f"Wrong compartment type {err}")
    

def check_bad_postsynaptic_compartment():    
    schema = PostsynapticCompartment()
    try:
        result = schema.load(bad_compartment)
        assert( result['compartment'] == 'soma' )
    except ValidationError as err:
        raise Exception(f"Wrong compartment type {err}")
    

def check_rich_postsynaptic_compartment():
    schema = PostsynapticCompartment()
    try:
        result = schema.load(rich_compartment)
        assert( result['on_spine'] )
    except ValidationError as err:
        raise Exception(f"Wrong compartment type {err}")
    