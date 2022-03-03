import marshmallow as mm
from emannotationschemas.schemas.base import (
    AnnotationSchema,
    BoundSpatialPoint,
    SpatialPoint,
)


class NucleusDetection(AnnotationSchema):
    volume = mm.fields.Float(description="the volume of the nucleus detected in um^3")
    pt = mm.fields.Nested(
        BoundSpatialPoint,
        required=True,
        description="the centroid of the nucleus, to be linked to the segmentation",
    )
    bb_start = mm.fields.Nested(
        SpatialPoint,
        required=False,
        description="low corner of the bounding box",
    )
    bb_end = mm.fields.Nested(
        SpatialPoint,
        required=False,
        description="high corner of the bounding box",
    )
