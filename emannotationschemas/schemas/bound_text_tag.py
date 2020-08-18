from emannotationschemas.schemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm

class BoundTagAnnotation(AnnotationSchema):
    pt = mm.fields.Nested(BoundSpatialPoint,
                         required=True,
                         description='Location associated with the tag')
    tag = mm.fields.String(required=True,
                           description='Arbitrary text tag')
    


