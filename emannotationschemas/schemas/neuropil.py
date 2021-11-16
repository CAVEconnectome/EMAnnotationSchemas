import marshmallow as mm
from emannotationschemas.schemas.base import ReferenceAnnotation


class NeuropilType(ReferenceAnnotation):
    neuropil = mm.fields.Str(
        required=True,
        description="type of neuropil",
    )
