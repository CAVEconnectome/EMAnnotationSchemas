from emannotationschemas.base import BoundSpatialPoint, \
    AnnotationSchema
from emannotationschemas.synapse import SynapseSchema
import marshmallow as mm

class ManualSynapseSchema(SynapseSchema):
  '''Direct copy of manual schemas'''
  obj_id = mm.fields.List(mm.fields.Int,
                          required=True,
                          description='List of object ids associated with synapse in the original data')
  synapse_category = mm.fields.String(required=False,
                              description='Synapse category')
  object_category = mm.fields.String(required=False,
                              description='Category of object of interest')

  @mm.post_load
  def validate_type(self, item):
    assert item['type'] == 'manual_synapse'
