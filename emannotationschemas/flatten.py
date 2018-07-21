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


def create_flattened_schema(BaseSchema, sep="_"):
    new_fields = flatten_fields(BaseSchema, sep=sep)
    FlatSchema = type('Flat{}'.format(BaseSchema.__name__),
                      (mm.Schema,),
                      new_fields)

    return FlatSchema
