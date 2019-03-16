from flask import Blueprint, jsonify, abort
from marshmallow_jsonschema import JSONSchema
from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas import get_schema, get_types
import marshmallow as mm
import pandas as pd

bp = Blueprint("schema", __name__, url_prefix="/schema")
__version__ = '2.0.0'


@bp.route("")
def index():
    return "EMAnnotationSchema -- version {}".format(__version__)


@bp.route("/version")
def get_version():
    return jsonify(__version__)


@bp.route("/type")
def get_schemas():
    return jsonify(get_types())


def get_type_schema(annotation_type):
    try:
        Schema = get_schema(annotation_type)
    except UnknownAnnotationTypeException:
        abort(404)
    json_schema = JSONSchema()
    js = json_schema.dump(Schema())
    return js.data


@bp.route("/type/<annotation_type>")
def get_type_schema_route(annotation_type):
    return jsonify(get_type_schema(annotation_type))


@bp.route("/type/<annotation_type>/view")
def get_schema_view(annotation_type):
    Schema = get_schema(annotation_type)
    print(dir(Schema))
    ds = []
    for col, field in Schema._declared_fields.items():
        if isinstance(field, mm.fields.Nested):
            print(dir(field.schema), field.schema)
            schema = field.schema.__class__.__name__
        else:
            schema = ''

        ds. append({
            'field_name': col,
            'description': field.metadata.get('description', ''),
            'type': type(field).__name__,
            'schema': schema
        })
    df = pd.DataFrame(ds)
    return df[['field_name', 'type', 'description', 'schema']].to_html()