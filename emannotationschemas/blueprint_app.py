from flask import abort
from flask_restx import Namespace, Resource
from marshmallow_jsonschema import JSONSchema

from emannotationschemas import get_schema, get_types
from emannotationschemas.errors import UnknownAnnotationTypeException

__version__ = "5.4.0"

authorizations = {
    "apikey": {"type": "apiKey", "in": "query", "name": "middle_auth_token"}
}

api_bp = Namespace(
    "EMAnnotation Schemas",
    authorizations=authorizations,
    description="EMAnnotation Schemas",
)


@api_bp.route("/type")
class SchemasTypes(Resource):
    @api_bp.doc("get_types", security="apikey")
    def get(self):
        return get_types()


def get_type_schema(annotation_type):
    try:
        Schema = get_schema(annotation_type)
    except UnknownAnnotationTypeException:
        abort(404)
    json_schema = JSONSchema()
    return json_schema.dump(Schema())


@api_bp.route("/type/<string:annotation_type>")
class SchemaAnnotationType(Resource):
    @api_bp.doc("get_annotation_type", security="apikey")
    def get(self, annotation_type: str):
        return get_type_schema(annotation_type)
