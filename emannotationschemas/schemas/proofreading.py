from emannotationschemas.schemas.base import (
    AnnotationSchema,
    BoundSpatialPoint,
    NumericField,
)
from marshmallow import fields, validate

proofread_choices = ["non", "clean", "extended"]
options_text = "Options are: 'non' to indicate no comprehensive proofreading, 'clean' to indicate comprehensive removal of false merges, and 'extended' to mean comprehensive extension of neurite tips"


class PointWithValid(AnnotationSchema):
    pt = fields.Nested(
        BoundSpatialPoint,
        required=True,
        description="Core location on proofread object",
    )
    valid_id = NumericField(
        required=True,
        description="Root id of the object when proofread status was assigned. If the pt_root_id of the cell differs, the proofreading status may not apply.",
    )


class ProofreadStatus(PointWithValid):
    status = fields.String(
        required=True,
        validate=validate.OneOf(proofread_choices),
        description=f"Proofread status of cell. {options_text}",
    )


class CompartmentProofreadStatus(PointWithValid):
    status_dendrite = fields.String(
        required=True,
        validate=validate.OneOf(proofread_choices),
        description=f"Proofread status of the dendrite only. {options_text}",
    )
    status_axon = fields.String(
        required=True,
        validate=validate.OneOf(proofread_choices),
        description=f"Proofread status of the axon only. {options_text}",
    )


class ProofreadingBoolStatus(PointWithValid):
    proofread = fields.Bool(
        required=True,
        description="Proofread status of cell.",
    )


class ProofreadingBoolStatusUser(ProofreadingBoolStatus):
    user_id = fields.Int(
        required=True,
        description="User who assessed the proofreading status.",
    )
