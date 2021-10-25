import marshmallow as mm
from emannotationschemas.schemas.base import ReferenceAnnotation
from marshmallow.validate import OneOf

allowed_compartments = [
    "soma",
    "dendrite",
    "axon",
]

allowed_dendrite_classes = ["basal", "apical"]


class PostsynapticCompartment(ReferenceAnnotation):

    compartment = mm.fields.Str(
        required=True,
        validate=OneOf(allowed_compartments),
        description="Compartment of the postsynaptic neuron \
                      targeted by the synapse",
    )

    on_spine = mm.fields.Bool(
        required=False,
        description="Boolean representing if the synapse is onto a spine or not",
    )

    dendrite_class = mm.fields.Str(
        required=False,
        validate=OneOf(allowed_dendrite_classes),
        description="Type of dendritic branch, e.g. basal or apical",
    )
