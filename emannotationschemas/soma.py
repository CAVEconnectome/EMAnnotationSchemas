from emannotationschemas.base import BoundSpatialPoint, \
    SpatialPoint, \
    AnnotationSchema
import marshmallow as mm


class Soma(AnnotationSchema):
    ctr_pt = mm.fields.Nested(BoundSpatialPoint, required=True,
                              description="central point",
                              order=1)
  
    min_point = mm.fields.Nested(SpatialPoint,
                                description='minimum corner point of a soma bounding box')
    max_point = mm.fields.Nested(SpatialPoint,
                                description='maximum corner point of a soma bounding box')
    volume = mm.fields.Float(description="volume of soma with a cutout around the central point, check bounds for cutout size")
    area = mm.fields.Float(description="area of soma with a cutout around the central point, check bounds for cutout size")
    soma_synapses = mm.fields.Int(description='number of synapses onto the cell based on the bounding box cutout, check bounds for cutout size')
    mean_synapse_size = mm.fields.Float(description="mean size of synapses onto the soma")
    median_synapse_size = mm.fields.Float(description="median size of synapses onto the soma")
    num_processes = mm.fields.Int(description='number of primary processes off of the soma')
    nucleus = mm.fields.Int(required=True, description = 'nucleus segmentation ID associated with the given cell ')

    @mm.post_load
    def validate_type(self, item):
        # check that the annotation type is present in the object as 'soma'
        assert item['type'] == 'soma'
        return item

