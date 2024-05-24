import marshmallow as mm
from emannotationschemas.schemas.base import (
    ReferenceTagAnnotation,
)

class ReferenceTagFloat(ReferenceTagAnnotation):
    value = mm.fields.Float(
        required=True, desription="Float value to be attached to the annotation"
    )
    