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
        pre_id = item['pre_pt'].get('root_id', None)
        post_id = item['post_pt'].get('root_id', None)
        if pre_id is not None:
            if (pre_id == post_id):
                item['valid'] = False
            else:
                item['valid'] = True
        return item
