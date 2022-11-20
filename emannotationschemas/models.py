from typing import Sequence

import marshmallow as mm
from geoalchemy2 import Geometry
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    MetaData,
    Table,
)
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from emannotationschemas import get_schema, get_types
from emannotationschemas.errors import (
    InvalidSchemaField,
    InvalidTableMetaDataException,
    UnknownAnnotationTypeException,
)
from emannotationschemas.flatten import create_flattened_schema
from emannotationschemas.schemas.base import (
    MetaDataTypes,
    NumericField,
    SegmentationField,
    PostGISField,
    ReferenceTableField,
)

from emannotationschemas.utils import create_segmentation_table_name


class ClassBase(object):
    @classmethod
    def __table_cls__(cls, *args, **kwargs):
        t = Table(*args, **kwargs)
        t.decl_class = cls
        return t


Base = declarative_base(cls=ClassBase)
FlatBase = declarative_base(cls=ClassBase)

field_column_map = {
    ReferenceTableField: BigInteger,
    NumericField: BigInteger,
    SegmentationField: BigInteger,
    PostGISField: Geometry,
    mm.fields.Int: Integer,
    mm.fields.Integer: Integer,
    mm.fields.Float: Float,
    mm.fields.Str: String,
    mm.fields.String: String,
    mm.fields.Bool: Boolean,
    mm.fields.Boolean: Boolean,
}


class ModelStore:
    def contains_model(self, table_name, flat=False):

        if flat:
            metadata_table = FlatBase.metadata.tables.get(table_name)
        else:
            metadata_table = Base.metadata.tables.get(table_name)
        if hasattr(metadata_table, "name"):
            metadata_table_name = metadata_table.name
        else:
            return None
        return table_name if table_name == metadata_table_name else None

    def get_model(self, table_name, flat=False):
        if flat:
            table = FlatBase.metadata.tables[table_name]
        else:
            table = Base.metadata.tables[table_name]
        return table.decl_class

    def reset_cache(self):
        Base.metadata.clear()
        FlatBase.metadata.clear()


sqlalchemy_models = ModelStore()


def format_database_name(aligned_volume: str, version: int = 0):
    return f"{aligned_volume}_v{version}"


def format_version_db_uri(sql_uri: str, aligned_volume: str, version: int = None):
    sql_uri_base = "/".join(sql_uri.split("/")[:-1])
    new_db_name = format_database_name(aligned_volume, version)
    return f"{sql_uri_base}/{new_db_name}"


def validate_types(schemas_and_tables: list):
    """Normalize a list of desired annotation types
    if passed None returns all types, otherwise checks that types exist

    Parameters
    ----------
    types: list[str] or None

    Returns
    -------
    list[str]
        list of types

    Raises
    ------
    UnknownAnnotationTypeException
        If types contains an invalid type
    """

    all_types = get_types()
    if any(
        schema_name not in all_types for schema_name, table_name in schemas_and_tables
    ):

        bad_types = [
            schema_name
            for schema_name, table_name in schemas_and_tables
            if schema_name not in all_types
        ]

        msg = f"{bad_types} are invalid types"
        raise UnknownAnnotationTypeException(msg)


def convert_dict_to_schema(schema_name: str, schema_dict: dict):
    """Generate a Marshmallow Schema object from dictionary.

    Parameters
    ----------
    schema_name : str
        Name of Schema to be used in object

    schema_dict : dict
        Dictionary of column types

    Returns
    -------
    Marshmallow Schema Object
    """
    return type(f"Flat{schema_name}", (mm.Schema,), schema_dict)


def split_annotation_schema(Schema):
    """Split an EM Annotation schema into separate annotation
    (spatial position) and segmentation (supervoxel and root_id) schemas

    Parameters
    ----------
    Schema : EMAnnotation Schema
        A Schema defined by EMAnnotationSchemas

    Returns
    -------
    flat_annotation_schema
        A flattened annotation marshmallow schema

    flat_segmentation_schema
        A flattened segmentation marshmallow schema

    Raises
    ------
    TypeError
        Schema is not flattened, i.e. nested schema type
    """

    flat_schema = create_flattened_schema(Schema)

    annotation_columns = {}
    segmentation_columns = {}

    for key, field in flat_schema._declared_fields.items():
        if isinstance(field, mm.fields.Nested):
            raise TypeError(
                f"Schema {flat_schema} must be flattened before splitting but contains nested fields"
            )

        if isinstance(field, SegmentationField):
            segmentation_columns[key] = field
        else:
            annotation_columns[key] = field
    schema_name = Schema.__name__ if hasattr(Schema, "__name__") else Schema
    flat_annotation_schema = convert_dict_to_schema(
        f"{schema_name}_annotation", annotation_columns
    )
    flat_segmentation_schema = convert_dict_to_schema(
        f"{schema_name}_segmentation", segmentation_columns
    )

    return flat_annotation_schema, flat_segmentation_schema


def create_sqlalchemy_model(
    table_name: str,
    Schema: mm.Schema,
    metadata_base: declarative_base,
    segmentation_source: str = None,
    table_metadata: dict = None,
    with_crud_columns: bool = False,
    reset_cache: bool = False,
) -> DeclarativeMeta:
    """Create a SQLAlchemy model from supplied
    marshmallow schema.

    Parameters
    ----------
    table_name : str
        Name of SQLAlchemy table.
    Schema : mm.Schema
        Marshmallow schema. Must be a valid type (hint see :func:`emannotationschemas.get_types`)
    segmentation_source : str, optional
        Filter model by segmentation columns, by default None
    table_metadata : dict, optional
        Supply additional columns, i.e. Reference Annotation Table, by default None
    with_crud_columns : bool, optional
        add additional created, deleted and superceded_id columns on
        an table model, by default False

    Returns
    -------
    DeclarativeMeta
        SQLAlchemy Model
    """

    table_dict = create_table_dict(
        table_name=table_name,
        Schema=Schema,
        segmentation_source=segmentation_source,
        table_metadata=table_metadata,
        with_crud_columns=with_crud_columns,
        reset_cache=reset_cache,
    )
    if reset_cache:
        metadata_base.metadata.clear()
    table_name = table_dict.get("__tablename__")
    return type(table_name, (metadata_base,), table_dict)


def create_table_dict(
    table_name: str,
    Schema: dict,
    segmentation_source: str = None,
    table_metadata: dict = None,
    with_crud_columns: bool = False,
    reset_cache: bool = False,
) -> dict:
    """Generate a dictionary of SQLAlchemy Columns that represent a table

    Parameters
    ----------
    table_name : str
        Combined name of an aligned_volume and specified table_name.
    Schema : EMAnnotation Schema
        A Schema defined by EMAnnotationSchemas
    table_metadata : dict, optional
        Supply additional columns, i.e. Reference Annotation Table, by default None
    with_crud_columns : bool, optional
        add additional created, deleted and superceded_id columns on
        an table model, by default False

    Returns
    -------
    model: dict
        Dictionary of sql column names and types

    Raises
    ------
    InvalidTableMetaDataException
    """
    model_dict = {}
    if segmentation_source:
        model_dict.update(
            {
                "__tablename__": create_segmentation_table_name(
                    table_name, segmentation_source
                ),
                "id": Column(
                    BigInteger, ForeignKey(f"{table_name}.id"), primary_key=True
                ),
                "__mapper_args__": {
                    "polymorphic_identity": create_segmentation_table_name(
                        table_name, segmentation_source
                    ),
                    "concrete": True,
                },
            }
        )
    else:
        model_dict.update(
            {
                "__tablename__": table_name,
                "id": Column(BigInteger, primary_key=True),
                "__mapper_args__": {
                    "polymorphic_identity": table_name,
                    "concrete": True,
                },
            }
        )
    if reset_cache:
        model_dict.update(
            {
                "__table_args__": {"extend_existing": True},
            }
        )

    if with_crud_columns:
        model_dict.update(
            {
                "created": Column(DateTime, index=True, nullable=False),
                "deleted": Column(DateTime, index=True),
                "superceded_id": Column(BigInteger),
            }
        )

    for key, field in Schema._declared_fields.items():
        if not field.metadata.get("drop_column", False):
            model_dict = validate_reference_table_metadata(
                model_dict, field, table_metadata
            )
            model_dict = add_column(model_dict, key, field)

    return model_dict


def add_column(model_dict: dict, key: str, field: str) -> dict:
    """Updates a dictionary with table column names as keys and
    the values being SqlAlchemy columns.

    Parameters
    ----------
    model_dict : dict
        dictionary of column name and types.
    key : str
        column name.
    field : str
        marshmallow schema field.

    Returns
    -------
    model_dict : dict
        dictionary of names and sqlalchemy columns.

    Raises
    ------
    InvalidSchemaField
        unsupported field type, not found in :data:`field_column_map`
    """
    field_type = type(field)
    has_index = field.metadata.get("index", False)
    if field_type in field_column_map:
        if field_type == PostGISField:
            postgis_geom = field.metadata.get("postgis_geometry", "POINTZ")
            model_dict[key] = Column(
                Geometry(
                    geometry_type=postgis_geom, dimension=3, use_N_D_index=has_index
                )
            )
        elif field_type == ReferenceTableField:
            reference_table_name = model_dict.pop("reference_table_name")
            foreign_key_name = f"{reference_table_name}.id"
            model_dict[key] = Column(
                BigInteger, ForeignKey(foreign_key_name), index=has_index
            )
        else:
            model_dict[key] = Column(field_column_map[field_type], index=has_index)

    else:
        raise InvalidSchemaField(f"field type {field_type} not supported")

    return model_dict


def validate_reference_table_metadata(
    model_dict: dict, field: str, table_metadata: dict = None
) -> dict:
    """Check if a supplied table metadata dict has correct
    formatting.

    Parameters
    ----------
    model_dict : dict
        dictionary of column name and types.
    field : str
        name of schema field.
    table_metadata : dict
        reference_table_name

    Returns
    -------
    model_dict: dict
        updates model_dict mapping to include 'reference_table_name'

    Raises
    ------
    InvalidTableMetaDataException
        The reference table metadata is missing or not a dict.
    """

    if field.metadata.get("field_type"):
        field_metadata = field.metadata.get("field_type")
    elif field.metadata.get("metadata"):
        metadata_dict = field.metadata.get("metadata")
        field_metadata = metadata_dict.get("field_type")
    else:
        field_metadata = None

    if field_metadata == MetaDataTypes.REFERENCE.value:
        if type(table_metadata) is not dict:
            msg = "no metadata provided for reference annotation"
            raise (InvalidTableMetaDataException(msg))
        else:
            try:
                model_dict["reference_table_name"] = table_metadata["reference_table"]
            except KeyError as e:
                msg = f"reference table not specified in metadata {table_metadata}: {e}"
                raise InvalidTableMetaDataException(msg)
    return model_dict


def make_annotation_model(
    table_name: str,
    schema_type: str,
    table_metadata: dict = None,
    with_crud_columns: bool = True,
    reset_cache: bool = False,
) -> DeclarativeMeta:
    """Make a SQLAlchemy annotation model from schema type.

    Parameters
    ----------
    table_name : str
        name of the annotation table
    schema_type : str
        schema type, must be a valid type (hint see :func:`emannotationschemas.get_types`)
    table_metadata : dict, optional
        optional metadata, by default None
    with_crud_columns : bool, optional
        add additional created, deleted and superceded_id columns on
        an annotation table model, by default True

    Returns
    -------
    DeclarativeMeta
        SQLAlchemy Model instance of the annotation
        columns of the schema
    """
    import warnings

    warnings.simplefilter("default")
    warnings.warn(
        "This method will be depreciated in future releases, see :func:'make_model_from_schema'",
        DeprecationWarning,
    )
    return make_model_from_schema(
        table_name=table_name,
        schema_type=schema_type,
        segmentation_source=None,
        table_metadata=table_metadata,
        with_crud_columns=with_crud_columns,
        reset_cache=reset_cache,
    )


def make_segmentation_model(
    table_name: str,
    schema_type: str,
    segmentation_source: str,
    table_metadata: dict = None,
    with_crud_columns: bool = False,
    reset_cache: bool = False,
) -> DeclarativeMeta:
    """Make a SQLAlchemy segmentation model from schema type.

    Parameters
    ----------

    table_name : str
        name of the table
    schema_type :
        schema type, must be a valid type (hint see :func:`emannotationschemas.get_types`)
    segmentation_source : str, optional
        pcg table to use for root id lookups will return the
        segmentation model if not None, by default None
    table_metadata : dict, optional
        optional metadata dict, by default None
    with_crud_columns : bool, optional
        add additional created, deleted and superceded_id columns on
        an annotation table model, by default False

    Returns
    -------
    DeclarativeMeta
        SQLAlchemy Model instance of the segmentation columns of the schema
    """
    import warnings

    warnings.simplefilter("default")
    warnings.warn(
        "This method will be depreciated in future releases",
        DeprecationWarning,
        stacklevel=2,
    )
    return make_model_from_schema(
        table_name=table_name,
        schema_type=schema_type,
        segmentation_source=segmentation_source,
        table_metadata=table_metadata,
        with_crud_columns=with_crud_columns,
        reset_cache=reset_cache,
    )


def make_reference_annotation_model(
    table_name: str,
    schema_type: str,
    target_table: str,
    segmentation_source: str = None,
    with_crud_columns: bool = True,
    reset_cache: bool = False,
) -> DeclarativeMeta:
    """Helper method to create reference annotation tables.

    Parameters
    ----------

    table_name : str
        name of the table
    schema_type :
        schema type, must be a valid type (hint see :func:`emannotationschemas.get_types`)
    target_table : str
        name of table to reference as a foreign key to its 'id' column
    segmentation_source : str, optional
        pcg table to use for root id lookups will return the
        segmentation model if not None, by default None
    with_crud_columns : bool, optional
        add additional created, deleted and superceded_id columns on
        an annotation table model, by default True

    Returns
    -------
    DeclarativeMeta
        SQLAlchemy Model instance of either the annotation
        or segmentation columns of the schema
    """
    import warnings

    warnings.simplefilter("default")
    warnings.warn(
        "This method will be depreciated in future releases",
        DeprecationWarning,
        stacklevel=2,
    )
    return make_model_from_schema(
        table_name=table_name,
        schema_type=schema_type,
        segmentation_source=segmentation_source,
        table_metadata={"reference_table": target_table},
        with_crud_columns=with_crud_columns,
        reset_cache=reset_cache,
    )


def make_model_from_schema(
    table_name: str,
    schema_type: str,
    segmentation_source: str = None,
    table_metadata: dict = None,
    with_crud_columns: bool = True,
    reset_cache: bool = False,
) -> DeclarativeMeta:
    """Create either the annotation or segmentation
    SQLAlchemy model from the supplied schema type.

    Notes
    -----
    If a segmentation source is included as an arg it will return
    the segmentation model of the schema.
    Will return either the columns that are defined as part of the annotations
    or segmentations but not both. To get a combined model see
    :func:`emannotationschemas.models.make_flat_model`

    Parameters
    ----------
    table_name : str
        name of the table
    schema_type :
        schema type, must be a valid type (hint see :func:`emannotationschemas.get_types`)
    segmentation_source : str, optional
        pcg table to use for root id lookups will return the
        segmentation model if not None, by default None
    table_metadata : dict, optional
        optional metadata dict, by default None
    with_crud_columns : bool, optional
        add additional created, deleted and superceded_id columns on
        an annotation table model, by default True
    reset_cache: bool, optional
        resets the sqlalchemy metadata and local cached model in case the target
        model changes, by default False

    Returns
    -------
    DeclarativeMeta
        SQLAlchemy Model instance of either the annotation
        or segmentation columns of the schema
    """
    Schema = get_schema(schema_type)
    annotation_schema, segmentation_schema = split_annotation_schema(Schema)
    if reset_cache:
        sqlalchemy_models.reset_cache()
    if not sqlalchemy_models.contains_model(table_name):
        anno_model = create_sqlalchemy_model(
            table_name=table_name,
            Schema=annotation_schema,
            metadata_base=Base,
            segmentation_source=None,
            table_metadata=table_metadata,
            with_crud_columns=with_crud_columns,
            reset_cache=reset_cache,
        )
    if segmentation_source:
        seg_table_name = create_segmentation_table_name(table_name, segmentation_source)
        if not sqlalchemy_models.contains_model(seg_table_name):

            seg_model = create_sqlalchemy_model(
                table_name=table_name,
                Schema=segmentation_schema,
                metadata_base=Base,
                segmentation_source=segmentation_source,
                table_metadata=table_metadata,
                with_crud_columns=False,
                reset_cache=reset_cache,
            )
        return sqlalchemy_models.get_model(seg_table_name)
    else:
        return sqlalchemy_models.get_model(table_name)


def make_flat_model(
    table_name: str,
    schema_type: str,
    table_metadata: dict = None,
    with_crud_columns: bool = False,
    reset_cache: bool = False,
) -> DeclarativeMeta:
    """Create a flattened model of combining both the annotation
    and segmentation columns into a single SQLAlchemy Model.

    Parameters
    ----------
    table_name : str
        name of the table
    schema_type : str
        schema type, must be a valid type (hint see :func:`emannotationschemas.get_types`)
    table_metadata : dict, optional
        optional metadata to attach to table, by default None
    with_crud_columns : bool, optional
        add additional created, deleted and superceded_id columns on
        an annotation table model, by default True
    reset_cache: bool, optional
        resets the sqlalchemy metadata and local cached model in case the target
        model changes, by default False
        
    Returns
    -------
    DeclarativeMeta
        SQLAlchemy Model instance
    """
    if reset_cache:
        sqlalchemy_models.reset_cache()
        FlatBase.metadata.clear()
    if not sqlalchemy_models.contains_model(table_name, flat=True):
        Schema = get_schema(schema_type)

        flat_schema = create_flattened_schema(Schema)

        flat_model = create_sqlalchemy_model(
            table_name=table_name,
            Schema=flat_schema,
            metadata_base=FlatBase,
            segmentation_source=None,
            table_metadata=table_metadata,
            with_crud_columns=with_crud_columns,
            reset_cache=reset_cache,
        )
    return sqlalchemy_models.get_model(table_name, flat=True)


def make_dataset_models(
    aligned_volume: str,
    schemas_and_tables: Sequence[tuple],
    segmentation_source: str = None,
    include_contacts: bool = False,
    metadata_dict: dict = None,
    with_crud_columns: bool = True,
    reset_cache: bool = False,
) -> dict:
    """Bulk create models for a given aligned_volume

    Parameters
    ----------
    aligned_volume: str
        name of aligned_volume

    table_and_types: list[(schema_name, table_name)]
        list of tuples with types and model names to make

    metadata_dict:
        a dictionary with keys of table_names and values of metadata dicts needed

    include_contacts:
        option to include the model for cell contacts

    with_crud_columns:
        option to include created, deleted, and superseded_id

    Returns
    -------
    dict:
        dictionary where keys are table_names and values are SQLAlchemy Models

    Raises
    ------
    UnknownAnnotationTypeException
        If a type is not a valid annotation type
    """
    validate_types(schemas_and_tables)
    dataset_dict = {}

    for schema_name, table_name in schemas_and_tables:
        model_key = table_name
        table_metadata = metadata_dict.get(model_key)
        dataset_dict[model_key] = make_model_from_schema(
            table_name,
            schema_name,
            segmentation_source,
            table_metadata,
            with_crud_columns,
            reset_cache,
        )
    if include_contacts:
        table_name = f"{aligned_volume}__contact"
        contact_model = make_model_from_schema(table_name, "contact")
        dataset_dict["contact"] = contact_model
    return dataset_dict
