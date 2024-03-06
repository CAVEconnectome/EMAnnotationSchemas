import marshmallow as mm
from emannotationschemas.schemas.base import AnnotationSchema, BoundSpatialPoint, NumericField
from emannotationschemas.schemas.bound_text_tag import BoundTagAnnotation

class BoundBoolAnnotation(AnnotationSchema):
    pt = mm.fields.Nested(
        BoundSpatialPoint, 
        required=True, 
        description="Location associated with the tag"
    )
    tag = mm.fields.Bool(required=True, description="Boolean at location")

class BoundBoolWithValid(BoundBoolAnnotation):
    valid_id = NumericField(
        required=True,
        description="Root id of the object when location was assessed. If the pt_root_id has changed, the associated segment has undergone proofreading.",
    )

class BoundTagWithValid(BoundTagAnnotation):
    valid_id = NumericField(
        required=True,
        description="Root id of the object when location was assessed. If the pt_root_id has changed, the associated segment has undergone proofreading.",
    )