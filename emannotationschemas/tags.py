from emannotationschemas.base import AnnotationSchema, \
                                     ReferenceAnnotation, \
                                     BoundSpatialPoint
import marshmallow as mm
from functools import partial

#Keeps track of the which types of objects for we allow reference tags.
referenceable_types = ['synapse','bouton_shape','bound_tag','reference_tag']

class TagAnnotation(mm.Schema):
    '''a simple text tag annotation'''
    tag = mm.fields.Str(
        required=True,description="Free text description")

class BoundTagAnnotation( AnnotationSchema, TagAnnotation ):
    '''A tag attached to a point in space.'''
    pt = mm.fields.Nested( BoundSpatialPoint, required=True,
                           description='Location associated with tag')
    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == 'bound_tag'

class ReferenceTagAnnotation(ReferenceAnnotation, TagAnnotation):
    '''A tag attached to another annotation'''
    target_id = mm.fields.Int(
        required=True,
        description='id of object tagged',
        reference_type="fill_in_with_reference_type"
        )

    valid_type = 'specify_valid_type'
    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == self.valid_type

@mm.post_load
def validate_type_helper( self, item, reference_tag_type ):
    assert item['type'] == reference_tag_type

def typed_reference_tag_factory(reference_type, ReferenceSchema ):
    new_tag_name = '{}_reference_tag'.format(reference_type)
    new_attrd = dict(ReferenceSchema.__dict__)
    new_attrd['_declared_fields']['target_id'] = mm.fields.Int(
                                    required=True,
                                    description='id of object tagged',
                                    reference_type=reference_type
                                    )
    new_attrd['valid_type'] = new_tag_name
    print(new_tag_name)
    return type(new_tag_name, (ReferenceSchema,), new_attrd)

TypedReferenceTags = {}
for ref_type in referenceable_types:
    TypedReferenceTags[ref_type] = typed_reference_tag_factory(ref_type, ReferenceTagAnnotation)
