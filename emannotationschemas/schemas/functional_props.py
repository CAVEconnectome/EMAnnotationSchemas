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
        required=True, description="preferred orientation in radians (0 - pi)"
    )
    pref_dir = mm.fields.Float(
        required=True, description="preferred direction in radians (0 - 2pi)"
    )
    gOSI = mm.fields.Float(
        required=True, description="global orientation selectivity index"
    )
    gDSI = mm.fields.Float(
        required=True, description="global direction selectivity index"
    )
    cc_abs = mm.fields.Float(
        required=True,
        description="prediction performance of the model, higher is better",
    )

class DigitalTwinPropertiesBCM(FunctionalPropertiesBCM):
    cc_abs = mm.fields.Float(
        required=True,
        description="Test set performance of the digital twin model unit, higher is better",
    )
    cc_max = mm.fields.Float(
        required=True,
        description="Neuron variability score used to normalize digital twin model unit performance",
    )
    cc_norm = mm.fields.Float(
        required=True,
        description="Normalized model unit performance, higher is better",
    )
    OSI = mm.fields.Float(
        required=True, description="orientation selectivity index"
    )
    DSI = mm.fields.Float(
        required=True, description="direction selectivity index"
    )
    pref_ori = mm.fields.Float(
        required=True, description="Preferred orientation in degrees (0 - 180), vertical bar moving right is 0 and orientation increases counter-clockwise"
    )
    pref_dir = mm.fields.Float(
        required=True, description="Preferred direction in degrees (0 - 360), vertical bar moving right is 0 and orientation increases counter-clockwise"
    )
    readout_loc_x = mm.fields.Float(
        required=True,
        description="X coordinate of the readout location, an approximation of receptive field center in stimulus space; (-1, -1) bottom-left, (1, 1) top-right",
    )
    readout_loc_y = mm.fields.Float(
        required=True,
        description="Y coordinate of the readout location, an approximation of receptive field center in stimulus space; (-1, -1) bottom-left, (1, 1) top-right",
    )
    # add readout weights?