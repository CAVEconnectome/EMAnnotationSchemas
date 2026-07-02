import marshmallow as mm

from emannotationschemas.schemas.base import ReferenceAnnotation


class ReferenceDoubleFloat(ReferenceAnnotation):
    value = mm.fields.Float(
        required=True, description="First float value attached to the annotation"
    )
    value2 = mm.fields.Float(
        required=True, description="Second float value attached to the annotation"
    )


class ReferenceTripleFloat(ReferenceAnnotation):
    value = mm.fields.Float(
        required=True, description="First float value attached to the annotation"
    )
    value2 = mm.fields.Float(
        required=True, description="Second float value attached to the annotation"
    )
    value3 = mm.fields.Float(
        required=True, description="Third float value attached to the annotation"
    )
