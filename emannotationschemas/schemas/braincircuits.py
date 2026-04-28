import marshmallow as mm
from emannotationschemas.schemas.base import AnnotationSchema, AutoUserIdField, BoundSpatialPoint


class BrainCircuitsBoundTagAnnotationUser(AnnotationSchema):
    pt = mm.fields.Nested(
        BoundSpatialPoint, required=True, description="Location associated with the tag"
    )
    tag = mm.fields.String(required=True, description="Arbitrary text tag")
    user_id = AutoUserIdField(
        required=True,
        description="User who created the tag, auto-populated from auth.",
    )
