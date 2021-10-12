import marshmallow as mm
from emannotationschemas.schemas.base import (
    AnnotationSchema,
    BoundSpatialPoint,
    NumericField,
)


class DerivedSpatialPoint(BoundSpatialPoint):
    dependent_chunk = NumericField(
        description="Chunk id for the point at the time the annotation was made",
        required=True,
    )
    level = NumericField(description="Chunk level", required=False)


class DerivedTag(AnnotationSchema):
    """Basic spatial tag using DerivedSpatialPoint information"""

    pt = mm.fields.Nested(DerivedSpatialPoint, required=True)
    tag = mm.fields.String(required=True, description="Description of point")


class DerivedNumeric(AnnotationSchema):
    """Floating point numeric value associated with a specific segmentation"""

    pt = mm.fields.Nested(DerivedSpatialPoint, required=True)
    value = mm.fields.Float(
        description="Numerical value specified by the table description"
    )
