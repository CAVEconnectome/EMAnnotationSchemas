from emannotationschemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm

class BoundSphere(AnnotationSchema):
    ctr_pt = mm.fields.Nested(BoundSpatialPoint,
                              required=True,
                              description='center of sphere')
    radius = mm.fields.Float(required=True,
                             description='radius of sphere')


    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == 'sphere'

        if item['radius'] >= 0:
            item['valid'] = True,
        else:
            item['valid'] = False