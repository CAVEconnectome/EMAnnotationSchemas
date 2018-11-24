from sqlalchemy import Column, String, Integer, Float, Numeric, Boolean, \
    DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2.shape import to_shape
from geoalchemy2 import Geometry
import shapely
from emannotationschemas import get_schema, get_types
from emannotationschemas.base import NumericField, ReferenceAnnotation
from emannotationschemas.contact import Contact
from emannotationschemas.errors import UnknownAnnotationTypeException, InvalidTableMetaDataException
import marshmallow as mm
import numpy as np

Base = declarative_base()

root_model_name = "CellSegment"


def format_table_name(dataset, table_name):
    return "{}_{}".format(dataset, table_name)


class ModelStore():

    def __init__(self):
        self.container = {}

    @staticmethod
    def to_key(dataset, table_name):
        return format_table_name(dataset, table_name)

    def contains_model(self, dataset, table_name):
        return self.to_key(dataset, table_name) in self.container.keys()

    def get_model(self, dataset, table_name):
        key = self.to_key(dataset, table_name)
        return self.container[key]

    def set_model(self, dataset, table_name, model):
        key = self.to_key(dataset, table_name)
        self.container[key] = model


annotation_models = ModelStore()

# TODO decide what to call this for real


class InvalidSchemaField(Exception):
    '''Exception raised if a schema can't be translated to a model'''


class AnalysisVersion(Base):
    __tablename__ = 'analysisversion'
    analysisversion_id = Column(Integer, primary_key=True)
    dataset = Column(String(100), nullable=False)
    version = Column(Integer, nullable=False)
    time_stamp = Column(DateTime, nullable=False)

    def __repr__(self):
        return "{}_v{}".format(self.dataset, self.version)


class AnalysisTable(Base):
    __tablename__ = 'analysistables'
    analysistable_id = Column(Integer, primary_key=True)
    schema_name = Column(String(100), nullable=False)
    table_name = Column(String(100), nullable=False)
    analysisversion_id = Column(Integer, ForeignKey('analysisversion.id'))
    analysisversion = relationship('AnalysisVersion')


class NumpyGeometry(Geometry):

    def bind_expression(self, value):
        str_rep = "{}({})".format(self.geometry_type, "{}".format(value)[1:-1])
        return super(NumpyGeometry, self).bind_expression(str_rep)

    def column_expression(self, value):
        wkb = super(NumpyGeometry, self).column_expression(value)
        shp = to_shape(wkb)
        if type(shp, shapely.geometry.Point):
            return np.array([shp.xy[0][0], shp.xy[1][0], shp.z], dtype=np.float)
        else:
            return shp

def validate_types(schemas_and_tables):
    '''normalize a list of desired annotation types
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
    '''

    all_types = get_types()
    if not (all(sn in all_types for sn, tn in schemas_and_tables)):
        bad_types = [sn for sn,
                     tn in schemas_and_tables if sn not in all_types]
        msg = '{} are invalid types'.format(bad_types)
        raise UnknownAnnotationTypeException(msg)


def make_dataset_models(dataset, schemas_and_tables, metadata_dict=None, include_contacts=False):
    """make all the models for a dataset

    Parameters
    ----------
    dataset: str
        name of dataset
    table_and_types: list[(schema_name, table_name)]
        list of tuples with types and model names to make
    metadata_dict:
        a dictionary with keys of table_names and values of metadata dicts needed
    include_contacts:
        option to include the model for cell contacts

    Returns
    -------
    dict
        dictionary where keys are table_names and values are sqlalchemy Models

    Raises
    ------
    UnknownAnnotationTypeException
        If a type is not a valid annotation type
    """
    if metadata_dict is None:
        metadata_dict = {}
    validate_types(schemas_and_tables)
    dataset_dict = {}
    cell_segment_model = make_cell_segment_model(dataset)
    dataset_dict[root_model_name.lower()] = cell_segment_model
    for schema_name, table_name in schemas_and_tables:
        model_key = table_name
        metadata = metadata_dict.get(table_name, None)
        dataset_dict[model_key] = make_annotation_model(dataset,
                                                        schema_name,
                                                        table_name,
                                                        table_metadata=metadata)
    if include_contacts:
        contact_model = make_annotation_model_from_schema(dataset,
                                                          'contact',
                                                          Contact)
        dataset_dict['contact'] = contact_model
    return dataset_dict


field_column_map = {
    NumericField: Numeric,
    mm.fields.Int: Integer,
    mm.fields.Integer: Integer,
    mm.fields.Float: Float,
    mm.fields.Str: String,
    mm.fields.String: String,
    mm.fields.Bool: Boolean,
    mm.fields.Boolean: Boolean
}


def add_column(attrd, k, field, dataset):
    field_type = type(field)
    do_index = field.metadata.get('index', False)
    if field_type in field_column_map:
        attrd[k] = Column(field_column_map[field_type], index=do_index)
    else:
        if isinstance(field, mm.fields.Nested):
            if field.many:
                raise InvalidSchemaField("Nested(many=True) not supported")
            for sub_k, sub_field in field.nested._declared_fields.items():
                do_sub_index = sub_field.metadata.get('index', False)
                postgis_geom = sub_field.metadata.get('postgis_geometry',
                                                      None)
                if postgis_geom:
                    attrd[k + "_" + sub_k] = Column(NumpyGeometry(postgis_geom,
                                                                  dimension=3))
                else:
                    dyn_args = [field_column_map[type(sub_field)]]
                    if sub_k == 'root_id':
                        table_name = format_table_name(dataset,
                                                       root_model_name.lower())
                        fk = table_name + ".id"
                        dyn_args.append(ForeignKey(fk))
                    attrd[k + "_" +
                          sub_k] = Column(*dyn_args,
                                          index=do_sub_index)
        else:
            raise InvalidSchemaField(
                "field type {} not supported".format(field_type))
    return attrd


def make_cell_segment_model(dataset):
    root_type = root_model_name.lower()
    attr_dict = {
        '__tablename__': format_table_name(dataset, root_type),
        root_model_name.lower()+'_id': Column(Numeric, primary_key=True, autoincrement=False),
        'version': Column(Integer, primary_key=True, autoincrement=False)
    }
    model_name = dataset.capitalize() + root_model_name

    if not annotation_models.contains_model(dataset, root_type):
        annotation_models.set_model(dataset,
                                    root_type,
                                    type(model_name, (Base,), attr_dict))
    return annotation_models.get_model(dataset, root_type)


def declare_annotation_model_from_schema(dataset, table_name, Schema, table_metadata=None):
    model_name = dataset.capitalize() + table_name.capitalize()
    attrd = {
        '__tablename__': format_table_name(dataset, table_name),
        table_name+'_id': Column(Numeric, primary_key=True, autoincrement=False),
        'version': Column(Integer, primary_key=True, autoincrement=False),
        '__mapper_args__': {
            'polymorphic_identity': dataset,
            'concrete': True
        }
    }
    for k, field in Schema._declared_fields.items():
        if (not field.metadata.get('drop_column', False)):
            attrd = add_column(attrd, k, field, dataset)
    if issubclass(Schema, ReferenceAnnotation):
        if type(table_metadata) is not dict:
            msg = 'no metadata provided for reference annotation'
            raise(InvalidTableMetaDataException(msg))
        else:
            try:
                reference_table_name = table_metadata['reference_table']
                reference_table = format_table_name(
                    dataset, reference_table_name)
            except KeyError:
                msg = 'reference table not specified in metadata {}'.format(
                    table_metadata)
                raise InvalidTableMetaDataException(msg)
        fk = ForeignKey(reference_table + '.' + reference_table_name+'_id')
        attrd[reference_table+'_id'] = Column(Numeric, fk, nullable=False)                                   
    return type(model_name, (Base,), attrd)


def make_annotation_model_from_schema(dataset,
                                      table_name,
                                      Schema,
                                      table_metadata=None):
    if not annotation_models.contains_model(dataset,
                                            table_name):
        Model = declare_annotation_model_from_schema(dataset,
                                                     table_name,
                                                     Schema,
                                                     table_metadata=table_metadata)
        annotation_models.set_model(dataset,
                                    table_name,
                                    Model)

    return annotation_models.get_model(dataset, table_name)


def declare_annotation_model(dataset, schema_name, table_name, table_metadata=None):
    Schema = get_schema(annotation_type)
    return declare_annotation_model_from_schema(dataset,
                                                table_name,
                                                Schema,
                                                table_metadata=table_metadata)


def make_annotation_model(dataset, schema_name, table_name, table_metadata=None):
    Schema = get_schema(schema_name)
    return make_annotation_model_from_schema(dataset,
                                             table_name,
                                             Schema,
                                             table_metadata=table_metadata)
