import marshmallow as mm
from emannotationschemas.schemas.base import (
    AnnotationSchema,
    BoundSpatialPoint,
    ReferenceAnnotation,
)


class FunctionalCoregistration(AnnotationSchema):
    pt = mm.fields.Nested(
        BoundSpatialPoint,
        required=True,
        description="location of cell body of functional cell",
    )
    func_id = mm.fields.Int(required=True, description="functional cell ID")




class FunctionalUnitCoregistration(AnnotationSchema):
    pt = mm.fields.Nested(
        BoundSpatialPoint,
        required=True,
        description="location of cell body of functional cell",
    )
    session = mm.fields.Int(required=True, description="session ID of imaging")
    scan_idx = mm.fields.Int(
        required=True, description="index of the scan within the session"
    )
    unit_id = mm.fields.Int(
        required=True, description="unique functional cell ID within the scan"
    )

class V1DDFunctionalUnitCoregistration(AnnotationSchema):
    pt = mm.fields.Nested(
        BoundSpatialPoint,
        required=True,
        description="location of cell body of functional cell",
    )
    column = mm.fields.Int(required=True, description="The index of the column, a set of volumes that were vertically stacked")
    volume = mm.fields.Int(
        required=True, description="index of the volume within the column"
    )
    plane = mm.fields.Int(
        required=False, description="index of imaging plane within the volume"
    )
    roi = mm.fields.Int(
        required=True, description="index of the roi within the plane"
    )
    residual = mm.fields.Float(
        required=False,
        description="distance between nucleus centroid and functional centroid after transformation",
    )
    score = mm.fields.Float(
        required=False, description="a confidence score associated with match"
    )


class FunctionalUnitCoregistrationExtended(ReferenceAnnotation):
    session = mm.fields.Int(required=True, description="session ID of imaging")
    scan_idx = mm.fields.Int(
        required=True, description="index of the scan within the session"
    )
    unit_id = mm.fields.Int(
        required=True, description="unique functional cell ID within the scan"
    )
    field = mm.fields.Int(
        required=False, description="index of imaging field of cell within the scan"
    )
    residual = mm.fields.Float(
        required=False,
        description="distance between nucleus centroid and functional centroid after transformation",
    )
    score = mm.fields.Float(
        required=False, description="confidence score associated with match"
    )


class FunctionalUnitCoregistrationQC(ReferenceAnnotation):
    pass
