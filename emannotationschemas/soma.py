from emannotationschemas.base import BoundSpatialPoint, \
    SpatialPoint, \
    AnnotationSchema
import marshmallow as mm


class SomaSchema(AnnotationSchema):
    ctr_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                              description="central point",
                              order=1)
  
    min_point = mm.fields.Nested(SpatialPoint,
                                description='minimum corner point of a soma bounding box')
    max_point = mm.fields.Nested(SpatialPoint,
                                description='maximum corner point of a soma bounding box')
    volume = mm.fields.Float(description="volume of soma with 15micron cutout around the central point")
    area = mm.fields.Float(description="area of soma with 15micron cutout around the central point")
    soma_synapses = mm.fields.Int(description='number of synapses onto the cell based on the bounding box cutout')
    mean_synase_size = mm.fields.Float(description="mean size of synapses onto the soma")
    median_synase_size = mm.fields.Float(description="median size of synapses onto the soma")
    num_processes = mm.fields.Int(description='number of primary processes off of the soma')

    @mm.post_load
    def validate_type(self, item):
        # check that the annotation type is present in the object as 'soma'
        assert item['type'] == 'soma'
        return item


class Nucleus(SomaSchema):
    cell_body = mm.fields.Int(required=True,
                            description = 'soma ')
