from flask_marshmallow import Marshmallow

ma = Marshmallow()

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