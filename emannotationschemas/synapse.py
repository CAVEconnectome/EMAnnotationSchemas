from emannotationschemas.base import BoundSpatialPoint, \
    SpatialPoint, \
    AnnotationSchema
import marshmallow as mm


class SynapseSchema(AnnotationSchema):
    pre_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                              description="presynaptic point",
                              order=0)
    ctr_pt = mm.fields.Nested(SpatialPoint, required=True,
                              description="central point",
                              order=1)
    post_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                               description="presynaptic point",
                               order=2)
    size = mm.fields.Float(description="size of synapse")

    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == 'synapse'
