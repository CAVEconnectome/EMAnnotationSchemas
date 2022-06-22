import marshmallow as mm
from emannotationschemas.schemas.base import ReferenceAnnotation


class SimpleGroup(ReferenceAnnotation):
    group_id = mm.fields.Int(
        required=True,
        description="group id",
    )
