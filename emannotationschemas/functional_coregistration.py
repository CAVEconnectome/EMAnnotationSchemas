from emannotationschemas.base import BoundSpatialPoint, \
    AnnotationSchema
import marshmallow as mm


class FunctionalCoregistration(AnnotationSchema):
    pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                          description="location of cell body of functional cell")
    func_id = mm.fields.Int(required=True, description="functional cell ID")

    @mm.post_load
    def validate_type(self, item):
        # check that the annotation type is present in the object as 'functional_coregistration'
        assert item['type'] == 'functional_coregistration'
