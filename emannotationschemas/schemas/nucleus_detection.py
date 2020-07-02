from emannotationschemas.schemas.base import FlatSegmentationReferenceSinglePoint
import marshmallow as mm

class NucleusDetection(FlatSegmentationReferenceSinglePoint):
    volume = mm.fields.Int(description="the volume of the nucleus detected in um^3")