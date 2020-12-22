from sqlalchemy import Column, String, Integer, Float, Numeric, Boolean, \
                       DateTime, ForeignKey, DateTime, BigInteger, Text, \
                       UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
import marshmallow as mm
from emannotationschemas import get_schema, get_types, get_flat_schema
from emannotationschemas.schemas.base import NumericField, PostGISField, \
                                     ReferenceAnnotation # SegmentationField
from emannotationschemas.schemas.contact import Contact
from emannotationschemas.flatten import create_flattened_schema
from emannotationschemas.errors import UnknownAnnotationTypeException, \
                                       InvalidTableMetaDataException, \
                                       InvalidSchemaField
from typing import Sequence
import logging

Base = declarative_base()
FlatBase = declarative_base()

field_column_map = {
    # SegmentationField: Numeric,
    NumericField: BigInteger,
    PostGISField: Geometry,
    mm.fields.Int: Integer,
    mm.fields.Integer: Integer,
    mm.fields.Float: Float,
    mm.fields.Str: String,
    mm.fields.String: String,
    mm.fields.Bool: Boolean,
    mm.fields.Boolean: Boolean
}


class ModelStore:

    def __init__(self):
        self.container = {}
        self.flat_container = {}

    def contains_model(self, table_name, flat=False):
        if flat:
            return table_name in self.flat_container.keys()
        else:
            return table_name in self.container.keys()

    def get_model(self, table_name, flat=False):
        if flat:
            return self.flat_container[table_name]
        else:
            return self.container[table_name]

    def set_model(self, table_name, model, flat=False):
        if flat:
            self.flat_container[table_name] = model
        else:
            self.container[table_name] = model


annotation_models = ModelStore()


def format_database_name(aligned_volume: str, version: int = 0):
    return f"{aligned_volume}_v{version}"


def format_version_db_uri(sql_uri: str, aligned_volume: str, version: int=None):
    sql_uri_base = "/".join(sql_uri.split('/')[:-1])
    new_db_name = format_database_name(aligned_volume, version)
    return sql_uri_base + f"/{new_db_name}"


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
    if not (all(schema_name in all_types for schema_name, table_name in schemas_and_tables)):
        
        bad_types = [schema_name for schema_name,
                     table_name in schemas_and_tables if schema_name not in all_types]
        
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
    return type(f'Flat{schema_name}', (mm.Schema,), schema_dict)

def split_annotation_schema(Schema):
    """ Split an EM Annotation schema into seperate annotation (spatial position) and 
    segmentation (supervoxel and root_id) schemas

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
    Exception
        Schema is not flattened, i.e. nested schema type
    """

    flat_schema = create_flattened_schema(Schema)

    annotation_columns = {}
    segmentation_columns = {}

    for key, field in flat_schema._declared_fields.items():
        if isinstance(field, mm.fields.Nested):
            raise Exception(f"Schema {flat_schema} must be flattened before splitting")
        field_type = type(field)

        if field_type is not NumericField:
            annotation_columns[key] = field   
        else:
            segmentation_columns[key] = field

    schema_name = Schema.__name__ if hasattr(Schema, '__name__') else Schema
    flat_annotation_schema = convert_dict_to_schema(f'{schema_name}_annotation',
                                                    annotation_columns)
    flat_segmentation_schema = convert_dict_to_schema(f'{schema_name}_segmentation',
                                                      segmentation_columns)

    return flat_annotation_schema, flat_segmentation_schema   


def create_segmentation_model(table_name: str,
                              segmentation_source: str,
                              segmentation_columns: dict):        
    """ Create an declarative sqlalchemy segmentation model that has
    a foriegn key linked to the supplied annotation_table_name.

    Parameters
    ----------
    table_name : str
        Combined name of an aligned_volume and specified table_name.
    pcg_table_name : str
    segmentation_columns : dict
    version : int, optional
        [description], by default 0

    Raises
    ------
    SqlAlchemy Declarative Base Model
        Segmentation SqlAlchemy model
    """

    segmentation_dict = create_table_dict(
        table_name, segmentation_columns, segmentation_source=segmentation_source, with_crud_columns=False)
    
    segmentation_table_name = segmentation_dict.get('__tablename__')

    SegmentationModel = type(segmentation_table_name, (Base,), segmentation_dict)
    return SegmentationModel


def create_annotation_model(table_name: str,
                            annotation_columns: dict,
                            with_crud_columns: bool=True):
    """ Create an declarative sqlalchemy annotation model.

    Parameters
    ----------
    table_name : str
        Specified table_name.

    annotation_columns : dict
        Dictionary of annotation SQL fields

    Returns
    -------
    SqlAlchemy Declarative Base Model
        Annotation SqlAlchemy model
    """
    annotation_dict = create_table_dict(table_name, 
                                        annotation_columns,
                                        with_crud_columns=with_crud_columns)
 
    annotation_name = annotation_dict.get('__tablename__')
   
    AnnotationModel = type(annotation_name, (Base,), annotation_dict)

    return AnnotationModel

def create_table_dict(table_name: str,
                      Schema: dict,
                      segmentation_source: str=None,
                      table_metadata: dict=None,
                      with_crud_columns: bool=True):
    """ Generate a dictionary of SQLAlchemy Columns that represent a table

    Parameters
    ----------
    table_name : str
        Combined name of an aligned_volume and specified table_name.

    Schema : EMAnnotation Schema
        A Schema defined by EMAnnotationSchemas

    table_metadata : dict, optional
        [description], by default None

    with_crud_columns : bool, optional
        [description], by default True

    Returns
    -------
    model: dict
        Dictionary of sql column names and types

    Raises
    ------
    InvalidTableMetaDataException
    """
    
    model = {}
    if segmentation_source:
        model.update({
        '__tablename__': f"{table_name}__{segmentation_source}",
        'id': Column(BigInteger, ForeignKey(f"{table_name}.id"), primary_key=True),
            '__mapper_args__': {
            'polymorphic_identity': f"{table_name}__{segmentation_source}",
            'concrete': True},
        })
    else:
        model.update({
            '__tablename__': table_name,
            'id': Column(BigInteger, primary_key=True),
            '__mapper_args__': {
                'polymorphic_identity': table_name,
                'concrete': True},
        })
    if with_crud_columns:
        model.update({
            'created': Column(DateTime, index=True, nullable=False),
            'deleted': Column(DateTime, index=True),
            'superceded_id': Column(BigInteger)
            })

    for key, field in Schema._declared_fields.items():
        if (not field.metadata.get('drop_column', False)):
            model = add_column(model, key, field)
    if issubclass(Schema, ReferenceAnnotation):
        target_field = Schema._declared_fields['target_id']
        if type(table_metadata) is not dict:
            msg = 'no metadata provided for reference annotation'
            raise(InvalidTableMetaDataException(msg))
        else:
            try:
                reference_table_name = table_metadata['reference_table']
                reference_table = table_name.split("__")[-1]
            except KeyError:
                msg = f"reference table not specified in metadata {table_metadata}"
                raise InvalidTableMetaDataException(msg)
            model['target_id'] = Column(Integer,
                                        ForeignKey(reference_table + '.id'))            
    return model


def add_column(columns: dict,
               key:str, 
               field:str) -> dict:   
    
    field_type = type(field)
    do_index = field.metadata.get('index', False)
    if field_type in field_column_map:
        if field_type == PostGISField:
            postgis_geom = field.metadata.get('postgis_geometry', 'POINTZ')
        
            columns[key] = Column(Geometry(geometry_type=postgis_geom, dimension=3))
        else:
            columns[key] = Column(field_column_map[field_type], index=do_index)
        
    else:
        raise InvalidSchemaField(f"field type {field_type} not supported")   
        
    return columns

def make_segmentation_model_from_schema(table_name: str,
                                        segmentation_source: str,
                                        Schema):
    segmentation_table_name = f"{table_name}__{segmentation_source}" 
    make_annotation_model_from_schema(table_name, Schema)

    if not annotation_models.contains_model(segmentation_table_name):
        __, segmentation_columns = split_annotation_schema(Schema)

        seg_model = create_segmentation_model(table_name,
                                              segmentation_source,
                                              segmentation_columns)
        annotation_models.set_model(segmentation_table_name, seg_model)

    return annotation_models.get_model(segmentation_table_name)

def make_annotation_model_from_schema(table_name: str,
                                      Schema,
                                      with_crud_columns: bool=True):
    
    if not annotation_models.contains_model(table_name):
        
        annotation_columns, __ = split_annotation_schema(Schema)

        anno_model = create_annotation_model(table_name,
                                       annotation_columns,
                                       with_crud_columns)       
        
        annotation_models.set_model(table_name,
                                    anno_model)

    return annotation_models.get_model(table_name)

def make_segmentation_model(table_name: str,
                            schema_type: str,
                            segmentation_source: dict=None):
    
    Schema = get_schema(schema_type)
    
    return make_segmentation_model_from_schema(table_name,
                                               segmentation_source,
                                               Schema)

def make_annotation_model(table_name: str,
                          schema_type: str,
                          with_crud_columns: bool=True):
    """make an annotation model

    Args:
        table_name (str): name of table in database
        schema_type (str): schema type for table
        version (int, optional): version number. Defaults to None.
        with_crud_columns (bool, optional): whether to include created, deleted colums. Defaults to True.

    Returns:
        SqlAlchemy.Model: a sqlalchemy model
    """
    Schema = get_schema(schema_type)
    
    return make_annotation_model_from_schema(table_name,
                                             Schema,
                                             with_crud_columns)

def make_flat_model_from_schema(table_name: str,
                                schema: str,
                                segmentation_source: dict=None):
    
    if not annotation_models.contains_model(table_name, flat=True):
        
        flat_schema = get_flat_schema(schema)
        
        annotation_dict = create_table_dict(
            table_name=table_name,
            Schema=flat_schema,
            segmentation_source=segmentation_source,
            table_metadata=None,
            with_crud_columns=False,
        )
        FlatAnnotationModel = type(table_name, (FlatBase,), annotation_dict)   
        
        annotation_models.set_model(table_name,
                                    FlatAnnotationModel, flat=True)

    return annotation_models.get_model(table_name, flat=True)


def make_flat_model(table_name: str,
                    schema_type: str,
                    segmentation_source: dict=None):

    return make_flat_model_from_schema(table_name,
                                       schema_type,
                                       segmentation_source)


def make_dataset_models(aligned_volume: str,
                        schemas_and_tables: Sequence[tuple],
                        include_contacts: bool = False,
                        version: int = None,
                        with_crud_columns: bool = True) -> dict:
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
        option to include created, deleted, and supersceded_id

    version: int
        option to include version number to use for making models, for legacy compatiabilty
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
        dataset_dict[model_key] = make_annotation_model(table_name,
                                                        schema_name)
    if include_contacts:
        table_name = f'{aligned_volume}__contact'                
        contact_model = make_annotation_model_from_schema(table_name,
                                                          Contact)
        dataset_dict['contact'] = contact_model
    return dataset_dict
