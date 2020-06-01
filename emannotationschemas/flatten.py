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
    
    schema_name = BaseSchema.__name__ if hasattr(BaseSchema, '__name__') else BaseSchema

    FlatSchema = type('Flat{}'.format(schema_name),
                      (mm.Schema,),
                      new_fields)

    return FlatSchema
