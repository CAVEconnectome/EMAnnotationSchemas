from emannotationschemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm


class GliaContact(AnnotationSchema):
    glia_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                              description="Glia-side point near a glia-object contact",
                              order=0)
    object_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                               description="Object-side point near a glia-object contact",
                               order=2)
    size = mm.fields.Float(description="size of contact", required=False)

    @mm.validates_schema
    def validate_type(self, data, **kwargs):
        # check that the annotation type is present in the object as 'glia_contact'
        if data["type"] != 'glia_contact':
            raise mm.ValidationError("Type must be 'glia_contact'")
