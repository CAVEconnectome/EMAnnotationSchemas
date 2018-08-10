from emannotationschemas.base import ReferenceAnnotation
import marshmallow as mm
from marshmallow.validate import OneOf

allowed_compartments = ['soma',
                        'shaft_apical',
                        'shaft_basal',
                        'shaft_unknown',
                        'spine_apical',
                        'spine_basal',
                        'spine_unknown',
                        'axon',
                        ]

class PostsynapticCompartment( ReferenceAnnotation ):

    target_id = mm.fields.Int(
        required=True,
        description='Synapse annotation id reference',
        reference_type='synapse')

    compartment = mm.fields.Str(
        required=True,
        validate=OneOf(allowed_compartments),
        description=['Compartment of the postsynaptic neuron \
                      targeted by the synapse']
        )

    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == 'postsynaptic_compartment'
