from emannotationschemas import base
from emannotationschemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm

field_lookup = {
    'int': mm.fields.Int
    'string': mm.fields.String,
    'float': mm.fields.Float,
    'BoundSpatialPoint': base.BoundSpatialPoint,
    'SpatialPoint': base.SpatialPoint,
    }

fields_to_nest = [base.SpatialPoint, base.BoundSpatialPoint]


def SimpleSchemaFactory(SchemaName, annotation_type, fields, descriptions={}, required={}, validation_rules=[]):
    _validate_arguments(SchemaName, annotation_type, fields, descriptions, required, validation_rules)
    
    class SimpleSchema(base.AnnotationSchema):
        @mm.post_load
        def validate_type(self, item):
            assert item['type'] == annotation_type
            for validation_rule in validation_rules:
                assert validation_rule(item)
        pass

    SimpleSchema.__name__ = SchemaName

    for field_name, field_type in fields.items():
        if field_type in fields_to_nest:
            SimpleSchema._declared_fields[field] = mm.fields.Nested(field_lookup[field_type](required=required.get(field_name, True),
                                                                            description=descriptions.get(field_name, ''))
                                                                    )
        else:
            SimpleSchema._declared_fields[field] = field_lookup[field_type](required=required.get(field_name, True),
                                                                            description=descriptions.get(field_name, '')                                                                        )
    return SimpleSchema


def CategoricalValidationFactory(allowed_category_dict):
    def categorical_validation(item):
        for category_name, allowed_categories in allowed_category_dict.items():
            if item[category_name] not in allowed_categories:
                return False
        else:
            return True
    return categorical_validation

def NonequalRootIDValidationFactory(nonequal_pair):
    def nonequal_validation(item):
        ptA = item[nonequal_pair[0]].get('root_id', None)
        ptB = item[nonequal_pair[1]].get('root_id', None)
        if ptA == ptB:
            return False
        else:
            return True
    return nonequal_validation


def _validate_arguments(SchemaName, annotation_type, fields, descriptions, required, validation_rules):
    if type(SchemaName) is not str:
        raise TypeError('SchemaName must be a string')

    if type(annotation_type) is not str:
        raise TypeError('annotation_type must be a string')

    for field in fields:
        if field not in field_lookup:
            raise ValueError('Field {} not in valid field list'.format(field))

    for d in descriptions:
        if type(d) is not str:
            raise TypeError('All descriptions must be strings')

    for r in required:
        if type(r) is not bool:
            raise TypeError('Requirements must be boolean')
    for validation_rule in validation_rules:
        if not callable(validation_rule):
            raise TypeError('All validation rules must be functions')
