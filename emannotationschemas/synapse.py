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
        # check that the annotation type is present in the object as 'synapse'
        assert item['type'] == 'synapse'

        pre_id = item['pre_pt'].get('root_id', None)
        post_id = item['post_pt'].get('root_id', None)

        # if the root_id is present
        # we should set the valid flag depending up on this rule
        # when the root_id is not present
        # (i.e. when posting new annotations with no root_id's in mind)
        # then the valid flag should be not present
        if pre_id is not None:
            if (pre_id == post_id):
                item['valid'] = False
            else:
                item['valid'] = True
        else:
            item.pop('valid', None)
        return item
