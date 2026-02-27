import marshmallow as mm
from marshmallow.validate import OneOf

from emannotationschemas.schemas.base import (
    AnnotationSchema,
    BoundSpatialPoint,
    ReferenceAnnotation,
)

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


class SpineWithInfo(AnnotationSchema):
    pt = mm.fields.Nested(
        BoundSpatialPoint,
        required=True,
        description="Spatial point representing the location of the spine",
    )
    
    volume = mm.fields.Float(
        required=False, description="Estimated volume of the spine"
    )

    n_inputs = mm.fields.Int(
        required=False,
        description="Number of synaptic inputs (unique root IDs) onto the spine",
    )

   
