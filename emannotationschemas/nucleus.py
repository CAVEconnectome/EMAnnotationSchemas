from emannotationschemas.base import BoundSpatialPoint, \
    SpatialPoint, \
    AnnotationSchema
import marshmallow as mm


class Nucleus(AnnotationSchema):
    ctr_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                              description="central point",
                              order=1)
    volume = mm.fields.Float(description="volume of nucleus")
    area = mm.fields.Float(description="surface area of nucleus")
    fold_fraction = mm.fields.Float(description="fraction of total surface area of nucleus within a nuclear fold")
    fold_area = mm.fields.Float(description="surface area of nucleus within a nuclear fold")
    cell_body = mm.fields.Int(required=True, description = 'cell body segmentation ID associated with the given nuclear ')

    @mm.post_load
    def validate_type(self, item):
        # check that the annotation type is present in the object as 'nucleus'
        assert item['type'] == 'nucleus'
        return item

