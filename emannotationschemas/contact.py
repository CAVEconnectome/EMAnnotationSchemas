from emannotationschemas.base import BoundSpatialPoint, \
    SpatialPoint, \
    AnnotationSchema
import marshmallow as mm

class Contact(AnnotationSchema):
    area = mm.fields.Float(description="contact area")
    sidea_pt = mm.fields.List(mm.fields.Int,
                              validate=mm.validate.Length(equal=3),
                              required=True,
                              description='spatial position in voxels of'
                                          'x,y,z of side a of contact',
                              postgis_geometry='POINTZ')
    sideb_pt = mm.fields.List(mm.fields.Int,
                              validate=mm.validate.Length(equal=3),
                              required=True,
                              description='spatial position in voxels of'
                                          'x,y,z of side b of contact',
                              postgis_geometry='POINTZ')
    sidea_supervoxel_ids = mm.fields.List(mm.fields.Int,
                                          description = "list of supervoxel ids on sidea")
    sideb_supervoxel_ids = mm.fields.List(mm.fields.List,
                                          description ="list of superevoxel ids assocaited with sideb")
                                          

    @mm.post_load
    def validate_type(self, item):
        # check that the annotation type is present in the object as 'synapse'
        assert item['type'] == 'contact'