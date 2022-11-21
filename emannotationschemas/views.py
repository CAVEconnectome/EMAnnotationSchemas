import marshmallow as mm
import pandas as pd
from flask import Blueprint, jsonify, render_template

from emannotationschemas import get_flat_schema, get_schema, get_types

__version__ = "5.4.1"


views_bp = Blueprint("views", __name__, url_prefix="/schema/views")


@views_bp.route("/")
def index():
    schema_types = get_types()

    return render_template("index.html", schema_types=schema_types, version=__version__)


@views_bp.route("/version")
def get_version():
    return jsonify(__version__)


@views_bp.route("/type/<annotation_type>/flatview")
def get_flat_schema_view(annotation_type):
    Schema = get_flat_schema(annotation_type)
    ds = []
    for col, field in Schema._declared_fields.items():
        if isinstance(field, mm.fields.Nested):
            print(dir(field.schema), field.schema)
            schema = field.schema.__class__.__name__
        else:
            schema = ""

        ds.append(
            {
                "field_name": col,
                "description": field.metadata.get("description", ""),
                "type": type(field).__name__,
                "schema": schema,
            }
        )
    df = pd.DataFrame(ds)
    return render_template(
        "schema.html",
        df_table=df[["field_name", "type", "description", "schema"]].to_html(),
        schema_type=annotation_type,
        version=__version__,
    )


@views_bp.route("/type/<annotation_type>/view")
def get_schema_view(annotation_type):
    Schema = get_schema(annotation_type)
    ds = []
    for col, field in Schema._declared_fields.items():
        if isinstance(field, mm.fields.Nested):
            print(dir(field.schema), field.schema)
            schema = field.schema.__class__.__name__
        else:
            schema = ""

        ds.append(
            {
                "field_name": col,
                "description": field.metadata.get("description", ""),
                "type": type(field).__name__,
                "schema": schema,
            }
        )
    df = pd.DataFrame(ds)
    return render_template(
        "schema.html",
        df_table=df[["field_name", "type", "description", "schema"]].to_html(),
        schema_type=annotation_type,
        version=__version__,
    )
