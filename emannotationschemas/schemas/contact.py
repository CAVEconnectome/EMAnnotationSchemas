from emannotationschemas.schemas.base import BoundSpatialPoint, \
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

    @mm.validates_schema
    def validate_type(self, data, **kwargs):
        # check that the annotation type is present in the object as 'contact'
        if data["type"] != 'contact':
            raise mm.ValidationError("Type must be 'contact'")

    @mm.post_load
    def check_contact_sides(self, data, **kwargs):
        sidea_id = data['sidea_pt'].get('root_id', None)
        sideb_id = data['sideb_pt'].get('root_id', None)
        # if the root_id is present
            # we should set the valid flag depending up on this rule
            # when the root_id is not present
            # (i.e. when posting new annotations with no root_id's in mind)
            # then the valid flag should be not present
        if sidea_id is not None:
            data['valid'] = False if sidea_id == sideb_id else True
        else:
            data.pop('valid', None)
        return data
