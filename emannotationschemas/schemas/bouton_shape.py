import marshmallow as mm
from emannotationschemas.schemas.base import ReferenceAnnotation
from marshmallow.validate import OneOf


class BoutonShape(ReferenceAnnotation):

    shape = mm.fields.Str(
        required=True,
        validate=OneOf(["pancake", "basmati", "potato"]),
        description="first example of description of a bouton shape",
    )
