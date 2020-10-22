from emannotationschemas.schemas.base import BoundSpatialPoint, NumericField, AnnotationSchema
import marshmallow as mm


class DerivedSpatialPoint(BoundSpatialPoint):
    dependent_chunk = NumericField(description='Layer 2 chunk id for the point at the time the annotation was made',
                                   required=True,
                                   segment=True)


class DerivedTag(AnnotationSchema):
    '''Basic spatial tag using DerivedSpatialPoint information'''
    pt = mm.fields.Nested(DerivedSpatialPoint, required=True)
    tag = mm.fields.String(required=True, description="Description of point")
