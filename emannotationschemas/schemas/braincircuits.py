import marshmallow as mm
from emannotationschemas.schemas.base import AnnotationSchema, BoundSpatialPoint


class BrainCircuitsBoundTagAnnotationUser(AnnotationSchema):
    pt = mm.fields.Nested(
        BoundSpatialPoint, required=True, description="Location associated with the tag"
    )
    tag = mm.fields.String(required=True, description="Arbitrary text tag")
    submission_time = mm.fields.DateTime(required=True, description="When the tag was submitted")
    user_id = mm.fields.String(
        required=True,
        description=f"User who created the tag.",
    )
