from marshmallow import fields, validate
from emannotationschemas.schemas.base import (
    BoundSpatialPoint,
    AnnotationSchema,
    NumericField,
)

proofread_choices = ["non", "clean", "extended"]


class PointWithValid(AnnotationSchema):
    pt = fields.Nested(
        BoundSpatialPoint,
        required=True,
        description="Core location on proofread object",
    )
    valid_root_id = NumericField(
        required=True,
        description="Root id of the object when proofread status was assigned. If the pt_root_id of the cell differs, the proofreading status may not apply.",
    )


class ProofreadStatus(PointWithValid):
    status = fields.String(
        required=True,
        validate=validate.OneOf(proofread_choices),
        description="Proofread status of cell",
    )


class NeuronProofreadStatus(PointWithValid):
    status_dendrite = fields.String(
        required=True,
        validate=validate.OneOf(proofread_choices),
        description="Proofread status of a cell dendrite",
    )
    status_axon = fields.String(
        required=True,
        validate=validate.OneOf(proofread_choices),
        description="Proofread status of a cell axon",
    )
