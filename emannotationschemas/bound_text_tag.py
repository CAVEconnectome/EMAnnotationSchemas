from emannotationschemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm
from marshmallow.validate import OneOf

class BoundTagAnnotation(AnnotationSchema):
    pt = mm.fields.Nested(BoundSpatialPoint,
                         required=True,
                         description='Location associated with the tag')
    tag = mm.fields.String(required=true,
                           description='Arbitrary text tag')
    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == 'bound_tag'
        return item