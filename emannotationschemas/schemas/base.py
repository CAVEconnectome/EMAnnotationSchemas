import marshmallow as mm
from geoalchemy2.shape import to_shape
from marshmallow import INCLUDE
from geoalchemy2.types import WKBElement, WKTElement
import numpy as np

class NumericField(mm.fields.Int):
    def _jsonschema_type_mapping(self):
        return {
            'type': 'integer',
        }

class PostGISField(mm.fields.Field):

    def _jsonschema_type_mapping(self):
        return {
            'type': 'array',
        }   
      
    def _deserialize(self, value, attr, obj, **kwargs):
        if isinstance(value, (WKBElement, WKTElement)):
            return get_geom_from_wkb(value)
        return value
    
    def _serialize(self, value, attr, obj, **kwargs):
        value = "POINTZ({} {} {})".format(value[0],
                                          value[1],
                                          value[2])
        return value

def get_geom_from_wkb(wkb):
    wkb_element = to_shape(wkb)
    if wkb_element.has_z:
        return np.asarray([wkb_element.xy[0][0],
                           wkb_element.xy[1][0], 
                           wkb_element.z], dtype=np.uint64)
    return wkb_element

class IdSchema(mm.Schema):
    '''schema with a unique identifier'''
    oid = mm.fields.Int(description='identifier for annotation, '
                                    'unique in type')


class AnnotationSchema(mm.Schema):
    class Meta:
        unknown = INCLUDE
    '''schema with the type of annotation'''

    valid = mm.fields.Bool(
        required=False,
        description="is this annotation valid",
        default=False,
        missing=None,
    )


class ReferenceAnnotation(AnnotationSchema):
    '''a annotation that references another annotation'''
    target_id = mm.fields.Int(
        required=True, description='annotation this references')


class FlatSegmentationReference(AnnotationSchema):
    pass


class TagAnnotation(mm.Schema):
    '''a simple tagged annotation'''
    tag = mm.fields.Str(
        required=True, description="tag to attach to annoation")


class ReferenceTagAnnotation(ReferenceAnnotation, TagAnnotation):
    '''A tag attached to another annotation'''


class SpatialPoint(mm.Schema):
    '''a position in the segmented volume '''
    
    position =  PostGISField(required=True,
                             description='spatial position in voxels of '
                                           'x,y,z of annotation',
                             postgis_geometry='POINTZ')
                             
    @mm.post_load
    def transform_position(self, data, **kwargs):
        if self.context.get('postgis', False):
            data['position'] = "POINTZ({} {} {})".format(data['position'][0],
                                             data['position'][1],
                                             data['position'][2])
        return data
    @mm.post_load
    def to_numpy(self, data, **kwargs):
        if self.context.get('numpy', False):
            data['position'] = np.asarray(data['position'], dtype=np.uint64)
        return data


class BoundSpatialPoint(SpatialPoint):
    ''' a position in the segmented volume that is associated with an object'''
    supervoxel_id = NumericField(missing=None,
                                 description="supervoxel id of this point", segment=True)
    root_id = NumericField(description="root id of the bound point", missing=None, segment=True,
                           index=True)

    @mm.post_load
    def convert_point(self, item, **kwargs):
        bsp_fn = self.context.get('bsp_fn', None)
        if bsp_fn is not None:
            bsp_fn(item)
        return item

class FlatSegmentationReferenceSinglePoint(FlatSegmentationReference):
    pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                          description="the point to be used for attaching objects to the dynamic segmentation")
