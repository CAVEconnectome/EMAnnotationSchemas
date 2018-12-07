from emannotationschemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm

class BoundTagAnnotation(AnnotationSchema):
    pt = mm.fields.Nested(BoundSpatialPoint,
                         required=True,
                         description='Location associated with the tag')
    tag = mm.fields.String(required=True,
                           description='Arbitrary text tag')
    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == 'bound_tag'
        return item
