import marshmallow as mm


def flatten_fields(schema, root=None, sep="_"):
    fields = {}
    if root is None:
        root = ""
    else:
        root = root + sep
    for k, field in schema._declared_fields.items():
        if isinstance(field, mm.fields.Nested):
            fields.update(flatten_fields(field.nested, root=root + k))
        else:
            fields[root + k] = field
    return fields


def flatten_dict(d, root=None, sep='_'):
    if root is None:
        root = ""
    else:
        root += sep
    d_out = {}
    for k, v in d.items():
        if type(v) is dict:
            fd = flatten_dict(v, root=root + k, sep=sep)
            d_out.update(fd)
        else:
            d_out[root + k] = v
    return d_out

def create_flattened_schema(BaseSchema, sep="_"):
    new_fields = flatten_fields(BaseSchema, sep=sep)
    
    schema_name = BaseSchema.__name__ if hasattr(BaseSchema, '__name__') else BaseSchema

    FlatSchema = type('Flat{}'.format(schema_name),
                      (mm.Schema,),
                      new_fields)

    return FlatSchema
