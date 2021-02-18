from emannotationschemas.schemas.base import BoundSpatialPoint, \
    SpatialPoint, \
    AnnotationSchema
from marshmallow import ValidationError
import marshmallow as mm


class SynapseSchema(AnnotationSchema):
    pre_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                              description="a nearby point located in the presynaptic compartment of the synase",
                              order=0)
    ctr_pt = mm.fields.Nested(SpatialPoint, required=True,
                              description="a point located near/on the synaptic contact",
                              order=1)
    post_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                               description="a nearby point located in the postsynaptic compartment of the synapse",
                               order=2)
    size = mm.fields.Float(description="size of synapse", missing=None)


    @mm.post_load
    def check_root_id(self, data, **kwargs):
        pre_id = data['pre_pt'].get('root_id', None)
        post_id = data['post_pt'].get('root_id', None)
        # when the root_id is present
        # we should set the valid flag depending up on this rule
        # when the root_id is not present
        # (i.e. when posting new annotations with no root_id's in mind)
        # then the valid flag should be not present
        if pre_id is not None:
            data['valid'] = False if pre_id == post_id else True
        else:
            data.pop('valid', None)
        return data
    

class PlasticSynapse(SynapseSchema):
    plasticity = mm.fields.Int(required=True,
                               validate=mm.validate.OneOf([0, 1, 2, 3, 4]),
                               description="plasticity state 0:not synapse 1:normal 2:mild 3:strong 4:not rated")
