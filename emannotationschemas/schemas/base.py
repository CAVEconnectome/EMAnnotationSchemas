from enum import Enum

import marshmallow as mm
import numpy as np
from geoalchemy2.shape import to_shape
from geoalchemy2.types import WKBElement, WKTElement
from marshmallow import INCLUDE
from sqlalchemy.sql.sqltypes import Integer


class MetaDataTypes(Enum):
    """Enum to hold custom marshmallow
    fields to facilitate SQLAlchemy model creation.
    """

    REFERENCE = "reference"
    ROOT_ID = "root_id"
    SPATIAL_POINT = "spatial_point"
    SUPERVOXEL_ID = "supervoxel_id"


class NumericField(mm.fields.Int):
    def _jsonschema_type_mapping(self):
        return {
            "type": "integer",
        }


class SegmentationField(NumericField):
    """Custom marshmallow field to specify the
    SQLAlchemy column is of a 'segmentation' type,
    i.e. a 'root_id' column or a 'supervoxel_id'
    """

    pass


class PostGISField(mm.fields.Field):
    def _jsonschema_type_mapping(self):
        return {
            "type": "array",
        }

    def _deserialize(self, value, attr, obj, **kwargs):
        if isinstance(value, (WKBElement, WKTElement)):
            return get_geom_from_wkb(value)
        return value

    def _serialize(self, value, attr, obj, **kwargs):
        value = f"POINTZ({value[0]} {value[1]} {value[2]})"
        return value


def get_geom_from_wkb(wkb):
    wkb_element = to_shape(wkb)
    if wkb_element.has_z:
        return np.asarray(
            [wkb_element.xy[0][0], wkb_element.xy[1][0], wkb_element.z], dtype=np.uint64
        )
    return wkb_element


class ReferenceTableField(mm.fields.Field):
    def _jsonschema_type_mapping(self):
        return {
            "type": "integer",
        }

    def _deserialize(self, value, attr, obj, **kwargs):
        if not isinstance(value, Integer):
            return int(value)
        return value

    def _serialize(self, value, attr, obj, **kwargs):
        return int(value)


class IdSchema(mm.Schema):
    """schema with a unique identifier"""

    oid = mm.fields.Int(description="identifier for annotation, unique in type")


class AnnotationSchema(mm.Schema):
    class Meta:
        unknown = INCLUDE

    """schema with the type of annotation"""

    valid = mm.fields.Bool(
        required=False,
        description="is this annotation valid",
        default=False,
        missing=None,
    )


class ReferenceAnnotation(AnnotationSchema):
    """a annotation that references another annotation"""

    target_id = ReferenceTableField(
        required=True,
        description="annotation this references",
        metadata={"field_type": MetaDataTypes.REFERENCE.value},
        index=True,
    )


class FlatSegmentationReference(AnnotationSchema):
    pass


class TagAnnotation(mm.Schema):
    """a simple tagged annotation"""

    tag = mm.fields.Str(required=True, description="tag to attach to annoation")


class ReferenceTagAnnotation(ReferenceAnnotation, TagAnnotation):
    """A tag attached to another annotation"""


class SpatialPoint(mm.Schema):
    """a position in the segmented volume"""

    position = PostGISField(
        required=True,
        description="spatial position in voxels of x,y,z of annotation",
        postgis_geometry="POINTZ",
        metadata={"field_type": MetaDataTypes.SPATIAL_POINT.value},
        index=True,
    )

    @mm.post_load
    def transform_position(self, data, **kwargs):
        if self.context.get("postgis", False):
            data[
                "position"
            ] = f'POINTZ({data["position"][0]} {data["position"][1]} {data["position"][2]})'

        return data

    @mm.post_load
    def to_numpy(self, data, **kwargs):
        if self.context.get("numpy", False):
            data["position"] = np.asarray(data["position"], dtype=np.uint64)
        return data


class BoundSpatialPoint(SpatialPoint):
    """a position in the segmented volume that is associated with an object"""

    supervoxel_id = SegmentationField(
        missing=None,
        description="supervoxel id of this point",
        metadata={"field_type": MetaDataTypes.SUPERVOXEL_ID.value},
        segmentation_field=True,
    )
    root_id = SegmentationField(
        description="root id of the bound point",
        missing=None,
        metadata={"field_type": MetaDataTypes.ROOT_ID.value},
        segmentation_field=True,
        index=True,
    )

    @mm.post_load
    def convert_point(self, item, **kwargs):
        bsp_fn = self.context.get("bsp_fn", None)
        if bsp_fn is not None:
            bsp_fn(item)
        return item


class FlatSegmentationReferenceSinglePoint(ReferenceAnnotation):
    """Bound spatial point reference to another annotation"""

    pt = mm.fields.Nested(
        BoundSpatialPoint,
        required=True,
        description="the point to be used for attaching objects to the dynamic segmentation",
    )
