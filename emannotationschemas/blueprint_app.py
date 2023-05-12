from flask import abort
from flask_restx import Namespace, Resource, reqparse
from marshmallow_jsonschema import JSONSchema

from emannotationschemas import get_schema, get_types
from emannotationschemas.errors import UnknownAnnotationTypeException

__version__ = "5.8.0"

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


def get_type_schemas():
    types = get_types()
    type_schemas = {}
    for type in types:
        type_schemas[type] = get_type_schema(type)
    return type_schemas


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


schema_parser = reqparse.RequestParser()
schema_parser.add_argument(
    "schema_names", type=str, action="split", help="list of schema names"
)


@api_bp.expect(schema_parser)
@api_bp.route("/type/schemas")
class SchemaAnnotationTypes(Resource):
    @api_bp.doc("get_annotation_types", security="apikey")
    def get(self):
        args = schema_parser.parse_args()
        schema_names = args.get("schema_names", None)
        if schema_names is not None:
            return {name: get_type_schema(name) for name in schema_names}
        else:
            return get_type_schemas()
