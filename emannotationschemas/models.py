from sqlalchemy import Column, String, Integer, Float, Numeric, Boolean, \
                       DateTime, ForeignKey, DateTime, BigInteger, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
import marshmallow as mm
from emannotationschemas import get_schema, get_types, get_flat_schema
from emannotationschemas.base import NumericField, PostGISField, \
                                     ReferenceAnnotation # SegmentationField
from emannotationschemas.flatten import create_flattened_schema
from emannotationschemas.contact import Contact
from emannotationschemas.errors import UnknownAnnotationTypeException, \
                                       InvalidTableMetaDataException, \
                                       InvalidSchemaField
from typing import Sequence

Base = declarative_base()

field_column_map = {
    #SegmentationField: Numeric,
    NumericField: Numeric,
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

    @staticmethod
    def to_key(dataset, table_name, version=None):
        return format_table_name(dataset, table_name, version)

    def contains_model(self, dataset, table_name, version=None):
        return self.to_key(dataset, table_name, version) in self.container.keys()

    def get_model(self, dataset, table_name, version=None):
        key = self.to_key(dataset, table_name, version)
        return self.container[key]

    def set_model(self, dataset, table_name, model, version=None):
        key = self.to_key(dataset, table_name, version)
        self.container[key] = model

annotation_models = ModelStore()

class Metadata(Base):
    __tablename__ = 'annotation_table_metadata'
    id = Column(Integer, primary_key=True)
    schema_type = Column(String(100), nullable=False)
    table_name = Column(String(100), nullable=False)
    valid = Column(Boolean)
    created = Column(DateTime, nullable=False)
    deleted = Column(DateTime, nullable=True)
    user_id = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    reference_table = Column(String(100), nullable=True)


def format_database_name(dataset: str, version: int = 1):
    return f"{dataset}_v{version}"


def format_version_db_uri(sql_uri: str, dataset: str, version: int=None):
    sql_uri_base = "/".join(sql_uri.split('/')[:-1])
    new_db_name = format_database_name(dataset, version)
    return sql_uri_base + f"/{new_db_name}"


def format_table_name(dataset, table_name, version=None):
    if version is not None:
        return f"{dataset}_{table_name}_v{version}"
    else:
        return f"{dataset}_{table_name}"

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

def create_linked_annotation_models(em_dataset: str,
                                   table_name: str, 
                                   annotation_columns: dict,
                                   segmentation_columns: dict):
    """ Create an annotation model which has a child segmentation model 
    with FK to primary key of the annotation table.

    Parameters
    ----------
    em_dataset : str
        Name of electron microscopy dataset name.

    table_name : str
        Name of table to use to define the __tablename__

    annotation_columns : dict
        Dictionary of annotation SQL fields

    segmentation_columns : dict
        Dictionary of segmentation SQL fields

    Returns
    -------
    SqlAlchemy Declarative Base Model
        Annotation SqlAlchemy model
    """
    annotation_dict = create_table_dict(em_dataset, table_name, annotation_columns)
    
    segmentation_dict = create_table_dict(em_dataset, table_name, segmentation_columns, with_crud_columns=False)
    
    annotation_name = annotation_dict.get('__tablename__', 'AnnotationSchema')
    segmentation_name = f"{annotation_name}_segmentation"
    try:
        segmentation_dict.pop('id')
    except KeyError:
        print(f"Segmentation Model {segmentation_dict} has no key 'id' ")
    
    segmentation_dict.update({
            '__tablename__': segmentation_name,
           'id': Column(Integer, primary_key=True),
           'annotation_id': Column(ForeignKey(f"{annotation_name}.id")),
           'annotation': relationship(annotation_name, lazy="joined")
    })   
    AnnotationModel = type(annotation_name, (Base,), annotation_dict)
    SegmentationModel = type(segmentation_name, (Base,), segmentation_dict)

    return AnnotationModel, SegmentationModel

def create_table_dict(em_dataset: str,
                      table_name: str,
                      Schema: dict,
                      table_metadata: dict=None,
                      version: int=None,
                      with_crud_columns: bool=True):
    """ Generate a dictionary of SQLAlchemy Columns that represent a table

    Parameters
    ----------
    em_dataset : str
        Name of electron microscopy dataset name.

    table_name : str
        Name of table to use to define the __tablename__

    Schema : EMAnnotation Schema
        A Schema defined by EMAnnotationSchemas

    table_metadata : dict, optional
        [description], by default None

    version : int, optional
        [description], by default None

    with_crud_columns : bool, optional
        [description], by default True

    Returns
    -------
    [type]
        [description]

    Raises
    ------
    InvalidTableMetaDataException
        [description]
    """
    model_name = em_dataset.capitalize() + table_name.capitalize()
    
    model = {}
    model.update({
        '__tablename__': format_table_name(em_dataset, 
                                           table_name,
                                           version=version),
        'id': Column(BigInteger, primary_key=True),
        '__mapper_args__': {
            'polymorphic_identity': em_dataset,
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
                reference_table = format_table_name(em_dataset,
                                                    reference_table_name,
                                                    version=version)
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
    segmentation_columns = {}

    if field_type in field_column_map:
        if field_type == PostGISField:
            postgis_geom = field.metadata.get('postgis_geometry', 'POINTZ')
        
            columns[key] = Column(Geometry(geometry_type=postgis_geom, dimension=3))
        else:
            columns[key] = Column(field_column_map[field_type], index=do_index)
        
    else:
        raise InvalidSchemaField(f"field type {field_type} not supported")   
        
    return columns

def create_model(Schema, em_dataset: str, table_name: str):
    """ This is a convenience method. Splits an EMAnnotation Schema into flattened annotation
    and segmentation schemas then creates a SqlAlchemy model. 
    
    See :meth:`emannotationschemas.models.split_annotation_schema` and
        :meth:`emannotationschemas.models.create_linked_annotation_model`
    
    Parameters
    ----------
    Schema : EMAnnotation Schema
        A Schema defined by EMAnnotationSchemas

    em_dataset : str
        Name of electron microscopy dataset name.

    table_name : str
        Name of table to use to define the __tablename__ 

    Returns
    -------
    SqlAlchemy Declarative Base Model
        Annotation SqlAlchemy model
    """
    annotation_columns, segmentation_columns = split_annotation_schema(Schema)
    
    return create_linked_annotation_models(em_dataset,
                                          table_name,
                                          annotation_columns,
                                          segmentation_columns)        

def make_annotation_model_from_schema(em_dataset: str,
                                      table_name: str,
                                      Schema,
                                      table_metadata: dict=None,
                                      version: int=None,
                                      with_crud_columns: bool=True):
    
    if not annotation_models.contains_model(em_dataset,
                                            table_name,
                                            version=version):
        
        Anno, Seg = create_model(Schema, em_dataset, table_name)
        
        
        annotation_models.set_model(em_dataset,
                                    table_name,
                                    Anno,
                                    version=version)

    return annotation_models.get_model(em_dataset, table_name, version=version)


def declare_annotation_model(em_dataset: str,
                             table_name: str,
                             schema_type: str,
                             table_metadata: dict=None,
                             version: int=None,
                             with_crud_columns: bool=True):
    
    Schema = get_schema(schema_type)
    return create_model(Schema, em_dataset, table_name)

def make_annotation_model(em_dataset: str,
                          table_name: str, 
                          schema_type: str,
                          table_metadata: dict=None,
                          version: int=None,
                          with_crud_columns: bool=True):
    
    Schema = get_schema(schema_type)
    
    return make_annotation_model_from_schema(em_dataset,
                                             table_name,
                                             Schema,
                                             table_metadata,
                                             version=None,
                                             with_crud_columns=with_crud_columns)


def make_dataset_models(em_dataset: str,
                        schemas_and_tables: Sequence[tuple],
                        table_metadata: dict=None,
                        include_contacts: bool=False,
                        version: int=None,
                        with_crud_columns: bool=True) -> dict:
    """Bulk create models for a given em_dataset

    Parameters
    ----------
    em_dataset: str
        name of dataset

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
    if table_metadata is None:
        table_metadata={}

    validate_types(schemas_and_tables)
    dataset_dict = {}

    for schema_name, table_name in schemas_and_tables:
        model_key = table_name
        metadata = table_metadata.get(table_name, None)
        dataset_dict[model_key] = make_annotation_model(em_dataset,
                                                        table_name,
                                                        schema_name,
                                                        metadata,
                                                        version,
                                                        with_crud_columns)
    if include_contacts:
        contact_model = make_annotation_model_from_schema(em_dataset,
                                                          'contact',
                                                          Contact,
                                                          metadata,
                                                          version, 
                                                          with_crud_columns)
        dataset_dict['contact'] = contact_model
    return dataset_dict
