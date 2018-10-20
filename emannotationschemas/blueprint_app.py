from flask import Blueprint, jsonify, abort
from marshmallow_jsonschema import JSONSchema
from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas import get_schema, get_types

bp = Blueprint("schema", __name__, url_prefix="/schema")


@bp.route("")
def get_schemas():
    return jsonify(get_types())


@bp.route("/<annotation_type>")
def get_type_schema(annotation_type):
    try:
        Schema = get_schema(annotation_type)
    except UnknownAnnotationTypeException:
        abort(404)
    json_schema = JSONSchema()
    js = json_schema.dump(Schema())
    return jsonify(js.data)
