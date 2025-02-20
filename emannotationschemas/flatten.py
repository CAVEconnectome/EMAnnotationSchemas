import marshmallow as mm


def flatten_fields(schema, root=None, sep="_"):
    fields = {}
    root = "" if root is None else root + sep
    for k, field in schema._declared_fields.items():
        if isinstance(field, mm.fields.Nested):
            nested_required = field.required
            nested_fields = flatten_fields(field.nested, root=root + k)
            
            if not nested_required:
                modified_fields = {}
                for field_name, nested_field in nested_fields.items():
                    new_field = type(nested_field)(
                        **{**nested_field.metadata, 
                           "required": False,
                           "allow_none": True,
                           "missing": None}
                    )
                    for attr in nested_field.__dict__:
                        if attr not in {"required", "allow_none", "missing", "metadata"}:
                            setattr(new_field, attr, getattr(nested_field, attr))
                    modified_fields[field_name] = new_field
                fields.update(modified_fields)
            else:
                fields.update(nested_fields)
        else:
            fields[root + k] = field
    return fields

def flatten_dict(d, root=None, sep="_"):
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

    schema_name = BaseSchema.__name__ if hasattr(BaseSchema, "__name__") else BaseSchema

    return type(f"Flat{schema_name}", (mm.Schema,), new_fields)
