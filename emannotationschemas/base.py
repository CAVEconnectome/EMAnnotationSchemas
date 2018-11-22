import marshmallow as mm


class NumericField(mm.fields.Int):
    def _jsonschema_type_mapping(self):
        return {
            'type': 'integer',
        }


class IdSchema(mm.Schema):
    '''schema with a unique identifier'''
    oid = mm.fields.Int(description='identifier for annotation, '
                                    'unique in type')


def flatten_dict(d, root=None, sep='_'):
    if root is None:
        root = ""
    else:
        root += sep
    d_out = {}
    for k, v in d.items():
        if type(v) is dict:
            fd = flatten_dict(v, root=root + k, sep=sep)
            d_out.update(fd)
        else:
            d_out[root + k] = v
    return d_out


class AnnotationSchema(mm.Schema):
    '''schema with the type of annotation'''
    type = mm.fields.Str(
        required=True,
        description='type of annotation',
        drop_column=True)

    valid = mm.fields.Bool(
        required=False,
        description="is this annotation valid"
    )


class ReferenceAnnotation(AnnotationSchema):
    '''a annoation that references another annotation'''
    target_id = mm.fields.Int(
        required=True, description='annotation this references')


class FlatSegmentationReference(ReferenceAnnotation):
    segment_id = mm.fields.Int(
        required=True, description='id in flat segmentation this should be linked to'
    )


class TagAnnotation(mm.Schema):
    '''a simple tagged annotation'''
    tag = mm.fields.Str(
        required=True, description="tag to attach to annoation")


class ReferenceTagAnnotation(ReferenceAnnotation, TagAnnotation):
    '''A tag attached to another annotation'''


class SpatialPoint(mm.Schema):
    '''a position in the segmented volume '''
    position = mm.fields.List(mm.fields.Int,
                              validate=mm.validate.Length(equal=3),
                              required=True,
                              description='spatial position in voxels of'
                                          'x,y,z of annotation',
                              postgis_geometry='POINTZ')

    @mm.post_load
    def transform_position(self, item):
        if self.context.get('postgis', False):
            item['position'] = "POINTZ({} {} {})".format(item['position'][0],
                                                         item['position'][1],
                                                         item['position'][2])
        return item


class BoundSpatialPoint(SpatialPoint):
    ''' a position in the segmented volume that is associated with an object'''
    supervoxel_id = NumericField(missing=mm.missing,
                                 description="supervoxel id of this point")
    root_id = NumericField(description="root id of the bound point",
                           index=True)

    @mm.post_load
    def convert_point(self, item):
        bsp_fn = self.context.get('bsp_fn', None)
        if bsp_fn is not None:
            bsp_fn(item)
        return item
