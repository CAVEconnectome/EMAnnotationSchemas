import marshmallow as mm
from emannotationschemas.schemas.base import ReferenceAnnotation
from marshmallow.validate import OneOf


class BoutonShape(ReferenceAnnotation):

    target_id = mm.fields.Int(
        required=True,
        description="annotation this references",
        reference_type="synapse",
    )

    shape = mm.fields.Str(
        required=True,
        validate=OneOf(["pancake", "basmati", "potato"]),
        description="first example of description of a bouton shape",
    )
