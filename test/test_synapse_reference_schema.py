from emannotationschemas.synapse import SynapseSchema
from emannotationschemas.presynaptic_bouton_type import PresynapticBoutonType
from emannotationschemas.postsynaptic_compartment import PostsynapticCompartment

from emannotationschemas.base import flatten_dict
from emannotationschemas import get_flat_schema

synapse_id = 1

good_bouton = {
    'type': 'presynaptic_bouton_type',
    'bouton_type': 'basmati',
    'target_id': synapse_id
    }

bad_bouton = {
    'type': 'presynaptic_bouton_type',
    'bouton_type': 'some_nonsense',
    'target_id': synapse_id
    }

good_compartment = {
    'type': 'postsynaptic_compartment',
    'compartment': 'soma',
    'target_id': synapse_id
    }

rich_compartment = {
    'type': 'postsynaptic_compartment',
    'compartment': 'dendrite',
    'on_spine' : True,
    'dendrite_class' : 'apical',
    'target_id': synapse_id
    }

bad_compartment = {
    'type': 'postsynaptic_compartment',
    'compartment': 'some_nonsense',
    'target_id': synapse_id
    }

def test_bouton_type():
    schema = PresynapticBoutonType()
    result = schema.load( good_bouton )
    assert(result.data['bouton_type'] == 'basmati' )

    result = schema.load( bad_bouton )
    assert('bouton_type' in result.errors)

def test_postsynaptic_compartment():
    schema = PostsynapticCompartment()
    result = schema.load( good_compartment )
    assert( result.data['compartment'] == 'soma' )

    result = schema.load( bad_compartment )
    assert('compartment' in result.errors)

    result = schema.load( rich_compartment )
    assert( result.data['on_spine'] )