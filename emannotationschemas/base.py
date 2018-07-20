import marshmallow as mm
from geoalchemy2.shape import from_shape, to_shape
from shapely import geometry


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
    for k,v in d.items():
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

    @mm.post_load
    def flatten_schema(self, item):
        if self.context.get('flatten', False):
            flatten_dict(item)


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


# class PointZ(mm.fields.List):
#     def _deserialize(self, value, attr, obj):
#         try:
            
#         except IndexError as e:
#             raise mm.ValidationError(
#                 'Cannot create pointz'.format(
#                     self.dtype))

#     def _serialize(self, value, attr, obj):
#         if value is None:
#             return None
#         list_ = list(to_shape(value).coords[0])
#         return mm.fields.List._serialize(self,
#                                          list_,
#                                          attr,
#                                          obj)

#     def _validate()
class SpatialPoint(mm.Schema):
    '''a position in the segmented volume '''
    position = mm.fields.Method('dump_geom',
                                deserialize='load_geom',
                                required=True,
                                description='spatial position in voxels of'
                                            'x,y,z of annotation',
                                postgis_geometry='POINTZ')
    
    def dump_geom(self, obj):
        return to_shape(obj).coords[0]

    def load_geom(self, value):
        if type(value) is not list:
            raise mm.ValidationError("only lists")
        if len(value) != 3:
            raise mm.ValidationError("not a pointz")

        return "POINTZ({} {} {})".format(value[0], value[1], value[2])


class BoundSpatialPoint(SpatialPoint):
    ''' a position in the segmented volume that is associated with an object'''
    supervoxel_id = mm.fields.Int(missing=mm.missing,
                                  description="supervoxel id of this point")
    root_id = mm.fields.Int(description="root id of the bound point",
                            index=True)

    @mm.post_load
    def convert_point(self, item):
        bsp_fn = self.context.get('bsp_fn', None)
        if bsp_fn is not None:
            bsp_fn(item)
