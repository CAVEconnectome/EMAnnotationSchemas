from emannotationschemas.schemas.base import BoundSpatialPoint, \
    AnnotationSchema
import marshmallow as mm


class FunctionalCoregistration(AnnotationSchema):
    pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                          description="location of cell body of functional cell")
    func_id = mm.fields.Int(required=True, description="functional cell ID")
