import marshmallow as mm

from emannotationschemas.base import BoundSpatialPoint

def get_flattened_bsp_keys_from_schema(schema):
    """ Returns the flattened keys of BoundSpatialPoints in a schema

    :param schema: schema
    :return: list
    """
    keys = []

    for key in schema.declared_fields.keys():
        field = schema.declared_fields[key]

        if isinstance(field, mm.fields.Nested) and \
                isinstance(field.schema, BoundSpatialPoint):
            keys.append("{}.{}".format(key, "position"))

    return keys