from emannotationschemas.base import BoundSpatialPoint, \
    SpatialPoint, \
    AnnotationSchema
import marshmallow as mm
# from marshmallow import validate


class SynapseSchema(AnnotationSchema):
    pre_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                              description="presynaptic point")
    ctr_pt = mm.fields.Nested(SpatialPoint, required=True,
                              description="central point")
    post_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                               description="presynaptic point")

    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == 'synapse'


# class BulkSynapse(mm.Schema):
#     pts = mm.fields.List(mm.fields.Float,
#                          required=True,
#                          validate=validate.Length(equal=9),
#                          description="pre(x,y,z) center(x,y,z) post(x,y,z)"
#                                      "position of synapse")

#     @mm.post_load
#     def unwrap_data(self, data):

#         pts = item.pop('pts')
#         item['pre_pt']={'position':pts[0:3]}
#         item['center_pt']={'position':pts[3:6]}
#         item['post_pt']={'position':pts[6:9]}
#         item['type']='synapse'
