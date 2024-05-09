import marshmallow as mm
from emannotationschemas.schemas.base import (
    ReferenceAnnotation,
)


class FunctionalPropertiesBCM(ReferenceAnnotation):
    session = mm.fields.Int(required=True, description="session ID of imaging")
    scan_idx = mm.fields.Int(
        required=True, description="index of the scan within the session"
    )
    unit_id = mm.fields.Int(
        required=True, description="unique functional cell ID within the scan"
    )
    pref_ori = mm.fields.Float(
        required=True, desription="preferred orientation in radians (0 - pi)"
    )
    pref_dir = mm.fields.Float(
        required=True, desription="preferred direction in radians (0 - 2pi)"
    )
    gOSI = mm.fields.Float(
        required=True, desription="global orientation selectivity index"
    )
    gDSI = mm.fields.Float(
        required=True, desription="global direction selectivity index"
    )
    cc_abs = mm.fields.Float(
        required=True,
        desription="prediction performance of the model, higher is better",
    )
