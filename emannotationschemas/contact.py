from emannotationschemas.base import BoundSpatialPoint, \
    SpatialPoint, \
    AnnotationSchema
import marshmallow as mm


class Contact(AnnotationSchema):
    size = mm.fields.Int(description="contact area (in units of voxel count)")
    sidea_pt = mm.fields.Nested(BoundSpatialPoint,
                                required=True,
                                description='point on sidea of contact')
    sideb_pt = mm.fields.Nested(BoundSpatialPoint,
                                required=True,
                                description='point on sideb of contact')
    ctr_pt = mm.fields.Nested(SpatialPoint,
                              description='point on contact interface')


    @mm.post_load
    def validate_type(self, item):
        # check that the annotation type is present in the object as 'synapse'
        assert item['type'] == 'contact'

        sidea_id = item['sidea_pt'].get('root_id', None)
        sideb_id = item['sideb_pt'].get('root_id', None)

        # if the root_id is present
        # we should set the valid flag depending up on this rule
        # when the root_id is not present
        # (i.e. when posting new annotations with no root_id's in mind)
        # then the valid flag should be not present
        if sidea_id is not None:
            if (sidea_id == sideb_id):
                item['valid'] = False
            else:
                item['valid'] = True
        else:
            item.pop('valid', None)
        return item
