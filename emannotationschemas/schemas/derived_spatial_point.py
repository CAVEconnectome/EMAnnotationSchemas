from emannotationschemas.schemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm


class DerivedSpatialPoint(AnnotationSchema):
    pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                          description="Location of annotated point")
    chunk_id = mm.fields.Int(required=True,
                             description="Layer 2 chunk id annotation depends on. If current layer 2 id differs, this annotation is potentially out of date")


class DerivedSpatialTag(DerivedSpatialPoint):
    tag = mm.fields.String(required=True, description="Descriptive text")
