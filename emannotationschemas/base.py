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

class PostGISField(mm.fields.Int):

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, (WKBElement, WKTElement)):
            return get_geom_from_wkb(value)
        return value


def get_geom_from_wkb(wkb):
    wkb_element = to_shape(wkb)
    if wkb_element.has_z:
        return f"POINTZ({wkb_element.xy[0][0]} {wkb_element.xy[1][0]} {wkb_element.z})"
    return wkb_element

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
    class Meta:
        unknown = INCLUDE
    '''schema with the type of annotation'''
    type = mm.fields.Str(
        required=True,
        description='type of annotation')

    valid = mm.fields.Bool(
        required=False,
        description="is this annotation valid",
        default=False,
        missing=None,
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
    position = PostGISField(postgis_geometry='POINTZ')
 

    @mm.post_load
    def transform_position(self, data, **kwargs):
        if self.context.get('postgis', False):
            data['position'] = "POINTZ({} {} {})".format(data['position'][0],
                                                         data['position'][1],
                                                         data['position'][2])
        return data

    @mm.post_load
    def transform_position(self, data, **kwargs):
        if self.context.get('numpy', False):
            data['position'] = np.asarray(data, dtype=np.uint64)

        return data

class BoundSpatialPoint(SpatialPoint):
    ''' a position in the segmented volume that is associated with an object'''
    supervoxel_id = NumericField(missing=None,
                                 description="supervoxel id of this point", segment=True)
    root_id = NumericField(description="root id TTT the bound point", missing=None, segment=True,
                           index=True)

    @mm.post_load
    def convert_point(self, item, **kwargs):
        bsp_fn = self.context.get('bsp_fn', None)
        if bsp_fn is not None:
            bsp_fn(item)
        return item
