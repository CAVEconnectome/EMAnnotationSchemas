from emannotationschemas.schemas.base import FlatSegmentationReferenceSinglePoint
from emannotationschemas.schemas.base import SpatialPoint
import marshmallow as mm


class NucleusDetection(FlatSegmentationReferenceSinglePoint):
    volume = mm.fields.Float(description="the volume of the nucleus detected in um^3")
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
