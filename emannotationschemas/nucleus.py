from emannotationschemas.base import BoundSpatialPoint, \
    SpatialPoint, \
    AnnotationSchema
import marshmallow as mm


class NucleusSchema(AnnotationSchema):
    ctr_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                              description="central point",
                              order=1)
  
    min_point = mm.fields.Nested(SpatialPoint,
                                description='minimum corner point of a nuclear bounding box')
    max_point = mm.fields.Nested(SpatialPoint,
                                description='maximum corner point of a nuclear bounding box')
    volume = mm.fields.Float(description="volume of nucleus")
    area = mm.fields.Float(description="surface area of nucleus")
    fold_fraction = mm.fields.Float(description="fraction of total surface area of nucleus within a nuclear fold")
    fold_area = mm.fields.Float(description="surface area of nucleus within a nuclear fold")
    cell_body = mm.fields.Int(required=True, description = 'cell body object associated with nuclear object ')

    @mm.post_load
    def validate_type(self, item):
        # check that the annotation type is present in the object as 'nucleus'
        assert item['type'] == 'nucleus'
        return item

