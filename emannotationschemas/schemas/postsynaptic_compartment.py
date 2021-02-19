from emannotationschemas.schemas.base import ReferenceAnnotation
import marshmallow as mm
from marshmallow.validate import OneOf
from marshmallow import validates_schema, ValidationError



allowed_compartments = ['soma',
                        'dendrite',
                        'axon',
                        ]

allowed_dendrite_classes = ['basal',
                            'apical']

class PostsynapticCompartment( ReferenceAnnotation ):

    target_id = mm.fields.Int(
        required=True,
        description='Synapse annotation id reference',
        reference_type='synapse')

    compartment = mm.fields.Str(
        required=True,
        validate=OneOf(allowed_compartments),
        description='Compartment of the postsynaptic neuron \
                      targeted by the synapse'
        )

    on_spine = mm.fields.Bool(
        required=False,
        description='Boolean representing if the synapse is onto a spine or not')

    dendrite_class = mm.fields.Str(
        required=False,
        validate=OneOf(allowed_dendrite_classes),
        description='Type of dendritic branch, e.g. basal or apical')

