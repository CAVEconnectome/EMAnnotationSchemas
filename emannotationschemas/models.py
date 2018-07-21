from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import AbstractConcreteBase
from geoalchemy2 import Geometry
from emannotationschemas import get_schema, get_types
import marshmallow as mm
Base = declarative_base()


class InvalidSchemaField(Exception):
    '''Exception raised if a schema can't be translated to a model'''


class TSBase(AbstractConcreteBase, Base):
    id = Column(Integer, primary_key=True)
    # @declared_attr
    # def table_name(cls):
    #     return Column(String(50), ForeignKey('locations.table_name'))


def make_all_models(datasets):
    model_dict = {}
    types = get_types()
    for dataset in datasets:
        model_dict[dataset] = {}
        for type_ in types:
            model_dict[dataset][type_] = make_annotation_model(dataset, type_)
    return model_dict


field_column_map = {
    mm.fields.Int: Integer,
    mm.fields.Float: Float,
    mm.fields.Str: String
}


def add_column(attrd, k, field):
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
                    attrd[k + "_" +
                          sub_k] = Column(field_column_map[type(sub_field)],
                                          index=do_sub_index)
        else:
            raise InvalidSchemaField(
                "field type {} not supported".format(field_type))
    return attrd


def make_annotation_model(dataset, annotation_type):
    Schema = get_schema(annotation_type)
    attrd = {
        '__tablename__': dataset + '_' + annotation_type,
        '__mapper_args__': {'polymorphic_identity': dataset, 'concrete': True}
    }
    for k, field in Schema._declared_fields.items():
        if (not field.metadata.get('drop_column', False)):
            attrd = add_column(attrd, k, field)

    model_name = dataset.capitalize() + annotation_type.capitalize()
    return type(model_name,
                (TSBase,),
                attrd)
