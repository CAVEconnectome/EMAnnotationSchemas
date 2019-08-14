from flask_marshmallow import Marshmallow
import marshmallow_sqlalchemy as msqla
import geoalchemy2
from shapely import geometry
from geoalchemy2.shape import from_shape, to_shape


ma = Marshmallow()

class GeometryField(fields.Field):
    """
    Use shapely and geoalchemy2 to serialize / deserialize a point
    Does make a big assumption about the data being spat back out as
    JSON, but what the hey.
    """

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        return geometry.mapping(to_shape(value))

    def _deserialize(self, value, attr, data):
        if value is None:
            return None
        return from_shape(geometry.shape(value))

msqla.ModelConverter.SQLA_TYPE_MAPPING[geoalchemy2.Geometry] = GeometryField

def make_annotation_flask_schema(model):
    model_name = model.__name__.capitalize() + "Schema"
    meta_attrd = {
        "model": model
    }
    metaclass = type("Meta", (), meta_attrd)
    attrd = {
        'Meta': metaclass,
    }
    return type(model_name, (ma.ModelSchema,), attrd)