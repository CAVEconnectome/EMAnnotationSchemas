from emannotationschemas.schemas.base import BoundSpatialPoint, \
    AnnotationSchema
import marshmallow as mm


class FunctionalCoregistration(AnnotationSchema):
    pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                          description="location of cell body of functional cell")
    func_id = mm.fields.Int(required=True, description="functional cell ID")

class FunctionalUnitCoregistration(AnnotationSchema):
    pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                          description="location of cell body of functional cell")
    session = mm.fields.Int(required=True, description="session ID of imaging")
    scan_idx = mm.fields.Int(required=True, description="index of the scan within the session")
    unit_id = mm.fields.Int(required=True, description="unique functional cell ID within the scan")

