from sqlalchemy import Column, String, Integer, Float, Numeric, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import AbstractConcreteBase
from geoalchemy2 import Geometry
from emannotationschemas import get_schema, get_types
from emannotationschemas.base import NumericField, ReferenceAnnotation
from emannotationschemas.contact import Contact
from emannotationschemas.errors import UnknownAnnotationTypeException
import marshmallow as mm
Base = declarative_base()


class ModelStore():

    def __init__(self):
        self.container = {}

    @staticmethod
    def to_key(dataset, type_):
        return dataset + "_" + type_

    def contains_model(self, dataset, type_):
        return self.to_key(dataset, type_) in self.container.keys()

    def get_model(self, dataset, type_):
        key = self.to_key(dataset, type_)
        return self.container[key]

    def set_model(self, dataset, type_, model):
        key = self.to_key(dataset, type_)
        self.container[key] = model


annotation_models = ModelStore()

# TODO decide what to call this for real
root_model_name = "CellSegment"


class InvalidSchemaField(Exception):
    '''Exception raised if a schema can't be translated to a model'''


class TSBase(AbstractConcreteBase, Base):
    id = Column(Integer, primary_key=True)
    # @declared_attr
    # def table_name(cls):
    #     return Column(String(50), ForeignKey('locations.table_name'))


def fix_types(types):
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
    if types is None:
        types = all_types
    else:
        if not (all(type_ in all_types for type_ in types)):
            msg = '{} contains invalid type'.format(types)
            raise UnknownAnnotationTypeException(msg)

    return types


def make_dataset_models(dataset, types=None, include_contacts=False):
    """make all the models for a dataset

    Parameters
    ----------
    dataset: str
        name of dataset
    types: list[str]
        list of types to make (default=None falls back to all types)
    include_contacts:
        option to include the model for cell contacts

    Returns
    -------
    dict
        dictionary where keys are types and values are sqlalchemy Models

    Raises
    ------
    UnknownAnnotationTypeException
        If a type is not a valid annotation type
    """

    types = fix_types(types)
    dataset_dict = {}
    cell_segment_model = make_cell_segment_model(dataset)
    dataset_dict[root_model_name.lower()] = cell_segment_model
    for type_ in types:
        dataset_dict[type_] = make_annotation_model(dataset, type_)
    if include_contacts:
        contact_model = make_annotation_model_from_schema(dataset,
                                                          'contact',
                                                          Contact)
        dataset_dict['contact'] = contact_model
    return dataset_dict


def make_all_models(datasets, types=None, include_contacts=False):
    """make all the models for a dataset

    Parameters
    ----------
    datasets: list[str]
        list of datasets to make models for
    types: list[str]
        list of types to make (default=None falls back to all types)
    include_contacts:
        option to include the model for cell contacts

    Returns
    -------
    dict
        2 level nested dictionary where first key is dataset,
        and second key is types and values are sqlalchemy Models


    Raises
    ------
    UnknownAnnotationTypeException
        If a type is not a valid annotation type
    """

    model_dict = {}
    types = fix_types(types)
    for dataset in datasets:
        model_dict[dataset] = make_dataset_models(dataset,
                                                  types,
                                                  include_contacts)
    return model_dict


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
                    attrd[k + "_" + sub_k] = Column(Geometry(postgis_geom,
                                                             dimension=3))
                else:
                    dyn_args = [field_column_map[type(sub_field)]]
                    if sub_k == 'root_id':
                        fk = dataset + "_" + root_model_name.lower() + ".root_id"
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
        '__tablename__': dataset + '_' + root_type,
        'root_id': Column(Numeric, index=True, unique=True)
    }
    model_name = dataset.capitalize() + root_model_name

    if not annotation_models.contains_model(dataset, root_type):
        annotation_models.set_model(dataset,
                                    root_type,
                                    type(model_name, (TSBase,), attr_dict))
    return annotation_models.get_model(dataset, root_type)


def make_annotation_model_from_schema(dataset, annotation_type, Schema):

    model_name = dataset.capitalize() + annotation_type.capitalize()

    if not annotation_models.contains_model(dataset, annotation_type):
        attrd = {
            '__tablename__': dataset + '_' + annotation_type,
            '__mapper_args__': {
                'polymorphic_identity': dataset,
                'concrete': True
            }
        }
        for k, field in Schema._declared_fields.items():
            if (not field.metadata.get('drop_column', False)):
                attrd = add_column(attrd, k, field, dataset)
        if issubclass(Schema, ReferenceAnnotation):
            target_field = Schema._declared_fields['target_id']
            reference_type = target_field.metadata['reference_type']
            attrd['target_id'] = Column(Integer, ForeignKey(
                dataset + '_' + reference_type + '.id'))
        annotation_models.set_model(dataset,
                                    annotation_type,
                                    type(model_name, (TSBase,), attrd))

    return annotation_models.get_model(dataset, annotation_type)


def make_annotation_model(dataset, annotation_type):
    Schema = get_schema(annotation_type)
    return make_annotation_model_from_schema(dataset, annotation_type, Schema)
