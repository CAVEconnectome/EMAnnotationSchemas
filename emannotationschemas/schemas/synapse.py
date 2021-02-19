from emannotationschemas.schemas.base import BoundSpatialPoint, \
    SpatialPoint, \
    AnnotationSchema
from marshmallow import ValidationError
import marshmallow as mm


class BaseSynapseSchema(AnnotationSchema):
    pre_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                              description="a nearby point located in the presynaptic compartment of the synase",
                              order=0)
    post_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                               description="a nearby point located in the postsynaptic compartment of the synapse",
                               order=2)


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

class SynapseSchema(BaseSynapseSchema):
    ctr_pt = mm.fields.Nested(SpatialPoint, required=True,
                              description="central point",
                              order=1)
    size = mm.fields.Float(description="size of synapse")


class BuhmannSynapseSchema(BaseSynapseSchema):
    score = mm.fields.Float(description="score assigned by Buhmann et al. 2019")
    cleft_score = mm.fields.Float(description="score derived by Buhmann et al. 2019 " \
                                  "by combining their synapses with the synapse " \
                                  "segmentation from Heinrich et al. 2018")


class BuhmannEcksteinSynapseSchema(BuhmannSynapseSchema):
    gaba = mm.fields.Float(description="Gaba probability by Eckstein et al. 2020")
    ach = mm.fields.Float(description="Acetylcholine probability by Eckstein et al. 2020")
    glut = mm.fields.Float(description="Glutamate probability by Eckstein et al. 2020")
    oct = mm.fields.Float(description="Octopamine probability by Eckstein et al. 2020")
    ser = mm.fields.Float(description="Serotonin probability by Eckstein et al. 2020")
    da = mm.fields.Float(description="Dopamine probability by Eckstein et al. 2020")
    valid_nt = mm.fields.Bool(description="False = no neurotransmitter prediction available.")


class PlasticSynapse(SynapseSchema):
    plasticity = mm.fields.Int(required=True,
                               validate=mm.validate.OneOf([0, 1, 2, 3, 4]),
                               description="plasticity state 0:not synapse 1:normal 2:mild 3:strong 4:not rated")
