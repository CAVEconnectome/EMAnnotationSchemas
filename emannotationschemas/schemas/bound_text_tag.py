from emannotationschemas.schemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm

class BoundTagAnnotation(AnnotationSchema):
    pt = mm.fields.Nested(BoundSpatialPoint,
                         required=True,
                         description='Location associated with the tag')
    tag = mm.fields.String(required=True,
                           description='Arbitrary text tag')
    
    @mm.validates_schema
    def validate_type(self, data, **kwargs):
        # check that the annotation type is present in the object as 'bound_tag'
        if data["type"] != 'bound_tag':
            raise mm.ValidationError("Type must be 'bound_tag'")

