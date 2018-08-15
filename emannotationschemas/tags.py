from emannotationschemas.base import AnnotationSchema, \
                                     ReferenceAnnotation, \
                                     BoundSpatialPoint
import marshmallow as mm

class TagAnnotation(mm.Schema):
    '''a simple text tag annotation'''
    tag = mm.fields.Str(
        required=True, description="Free text description")

class ReferenceTagAnnotation(AnnotationSchema, ReferenceAnnotation, TagAnnotation):
    '''A tag attached to another annotation'''
    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == 'reference_tag'

class BoundTagAnnotation(AnnotationSchema, BoundSpatialPoint, TagAnnotation ):
    '''A tag attached to a point in space.'''
    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == 'bound_tag'