import marshmallow as mm
from emannotationschemas.schemas.base import ReferenceAnnotation


class FlyNeuropil(ReferenceAnnotation):
    neuropil = mm.fields.Str(
        required=True,
        description="neuropil name",
    )
