from emannotationschemas.base import AnnotationSchema, \
                                     ReferenceAnnotation, \
                                     BoundSpatialPoint
import marshmallow as mm

class TagAnnotation(mm.Schema):
    '''a simple text tag annotation'''
    tag = mm.fields.Str(
        required=True,description="Free text description")

class ReferenceTagAnnotation(ReferenceAnnotation, TagAnnotation):
    '''A tag attached to another annotation'''
    target_id = mm.fields.Int(
        required=True,
        description='id of object tagged',
        reference_type='any')

    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == 'reference_tag'

class BoundTagAnnotation( AnnotationSchema, TagAnnotation ):
    '''A tag attached to a point in space.'''
    pt = mm.fields.Nested( BoundSpatialPoint, required=True,
                           description='Location associated with tag')
    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == 'bound_tag'