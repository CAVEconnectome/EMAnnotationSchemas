from flask import Blueprint, jsonify, request, abort, current_app, g
from flask_restx import Namespace, Resource, reqparse, fields
from flask_accepts import accepts, responds
from middle_auth_client import auth_required, auth_requires_permission

from marshmallow_jsonschema import JSONSchema
from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas import get_schema, get_types
import marshmallow as mm
import pandas as pd


__version__ = '3.1.1'

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'query',
        'name': 'middle_auth_token'
    }
}

api_bp = Namespace("EMAnnotation Schemas",
                   authorizations=authorizations,
                   description="EMAnnotation Schemas")


@api_bp.route("/type")
class SchemasTypes(Resource):
   
    @auth_required
    @api_bp.doc('get_types', security='apikey')
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
   
    @auth_required
    @api_bp.doc('get_annotation_type', security='apikey')
    def get(self, annotation_type: str):
        return get_type_schema(annotation_type)
