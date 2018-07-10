import marshmallow as mm


class IdSchema(mm.Schema):
    '''schema with a unique identifier'''
    oid = mm.fields.Int(description='identifier for annotation, '
                                    'unique in type')


class AnnotationSchema(mm.Schema):
    '''schema with the type of annotation'''
    type = mm.fields.Str(
        required=True, description='type of annotation')


class IdAnnotationSchema(IdSchema, AnnotationSchema):
    '''base schema for annotations'''
    pass


class ReferenceAnnotation(mm.Schema):
    '''a annoation that references another annotation'''
    target_id = mm.fields.Int(
        required=True, description='annotation this references')


class TagAnnotation(mm.Schema):
    '''a simple tagged annotation'''
    tag = mm.fields.Str(
        required=True, description="tag to attach to annoation")


class ReferenceTagAnnotation(ReferenceAnnotation, TagAnnotation):
    '''A tag attached to another annotation'''


class SpatialPoint(mm.Schema):
    '''a position in the segmented volume '''
    position = mm.fields.List(mm.fields.Int,
                              required=True,
                              validate=mm.validate.Length(equal=3),
                              description='spatial position in voxels of'
                                          'x,y,z of annotation')


class BoundSpatialPoint(SpatialPoint):
    ''' a position in the segmented volume that is associated with an object'''
    supervoxel_id = mm.fields.Int(missing=mm.missing,
                                  description="supervoxel id of this point")
    root_id = mm.fields.Int(description="root id of the bound point")

    @mm.post_load
    def convert_point(self, item):
        bsp_fn = self.context.get('bsp_fn', None)
        if bsp_fn is not None:
            bsp_fn(item)
