from flask import jsonify, render_template, current_app, make_response, Blueprint
from emannotationschemas import get_schema

from emannotationschemas import get_schema, get_types
import marshmallow as mm
import pandas as pd


import pandas as pd
import os

__version__ = '2.0.2'


views_bp = Blueprint('views', __name__, url_prefix='/schema/views')

@views_bp.route("/")    
def index():
    return "EMAnnotationSchema -- version {}".format(__version__)


@views_bp.route("/version")
def get_version():
    return jsonify(__version__)


@views_bp.route("/type/<annotation_type>/view")
def get_schema_view(annotation_type):
    Schema = get_schema(annotation_type)
    ds = []
    for col, field in Schema._declared_fields.items():
        if isinstance(field, mm.fields.Nested):
            print(dir(field.schema), field.schema)
            schema = field.schema.__class__.__name__
        else:
            schema = ''

        ds.append({
            'field_name': col,
            'description': field.metadata.get('description', ''),
            'type': type(field).__name__,
            'schema': schema
        })
    df = pd.DataFrame(ds)
    return df[['field_name', 'type', 'description', 'schema']].to_html()