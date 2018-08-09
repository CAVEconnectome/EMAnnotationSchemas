from emannotationschemas.base import ReferenceAnnotation
import marshmallow as mm
from marshmallow.validate import OneOf


class BoutonShape(ReferenceAnnotation):

    target_id = mm.fields.Int(
        required=True,
        description='annotation this references',
        reference_type='synapse')

    shape = mm.fields.Str(
        required=True,
        validate=OneOf(["pancake", "basmati", "potato"]),
        description="first example of description of a bouton shape")

    @mm.post_load
    def validate_type(self, item):
        # check that the annotation type is present in the object as 'synapse'
        assert item['type'] == 'bouton_shape'
