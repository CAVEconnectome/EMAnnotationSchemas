from emannotationschemas.base import BoundSpatialPoint, \
    AnnotationSchema
import marshmallow as mm


class FunctionalCoregistration(AnnotationSchema):
    pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                          description="location of cell body of functional cell")
    func_id = mm.fields.Int(required=True, description="functional cell ID")

    @mm.validates_schema
    def validate_type(self, data, **kwargs):
        # check that the annotation type is present in the object as 'microns_func_coreg'
        if data["type"] != 'microns_func_coreg':
            raise mm.ValidationError("Type must be 'microns_func_coreg'")
