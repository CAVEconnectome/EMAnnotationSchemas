import marshmallow as mm
from emannotationschemas.schemas.base import ReferenceAnnotation
from marshmallow.validate import OneOf

allowed_bouton_categories = [
    "pancake",
    "basmati",
    "potato",
    "sst",
    "vertical",
    "vip",
    "ivy",
    "clutch",
    "chandelier",
]


class PresynapticBoutonType(ReferenceAnnotation):

    bouton_type = mm.fields.Str(
        required=True,
        validate=OneOf(allowed_bouton_categories),
        description="Presynaptic type based on bouton",
    )
