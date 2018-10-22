from flask import Blueprint, jsonify, abort
from marshmallow_jsonschema import JSONSchema
from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas import get_schema, get_types
from flask import jsonify


bp = Blueprint("schema", __name__, url_prefix="/schema")
__version__ = '0.3.3'

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
