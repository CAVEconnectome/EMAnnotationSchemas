from emannotationschemas import base
from emannotationschemas.validation_factories import validation_func_lookup
import marshmallow as mm

field_lookup = {
    'int': mm.fields.Int,
    'string': mm.fields.String,
    'float': mm.fields.Float,
    'boolean': mm.fields.Boolean,
    'BoundSpatialPoint': base.BoundSpatialPoint,
    'SpatialPoint': base.SpatialPoint,
    }

fields_to_nest = ['SpatialPoint', 'BoundSpatialPoint']

def SimpleSchemaFactory(SchemaName,
                        annotation_type,
                        fields,
                        descriptions={},
                        required={},
                        kwarg_dict={},
                        validation_rules={}):
    _validate_arguments(SchemaName, annotation_type, fields, descriptions, required, validation_rules)
    class SimpleSchema(base.AnnotationSchema):
        @mm.post_load
        def validate_type(self, item):
            assert item['type'] == annotation_type
            valid = []
            for validation_rule, args in validation_rules.items():
                validation_func = validation_func_lookup[validation_rule](*args)
                valid.append(validation_func(item))
            if None in valid:
                item.pop('valid', None)
            elif all(valid):
                item['valid'] = True
            else:
                item['valid'] = False 
            return item
        pass

    SimpleSchema.__name__ = SchemaName

    for field_name, field_type in fields.items():
        if field_type in fields_to_nest:
            SimpleSchema._declared_fields[field_name] = mm.fields.Nested(field_lookup[field_type],
                                                                         required=required.get(field_name, False),
                                                                         description=descriptions.get(field_name, ''),
                                                                         **kwarg_dict.get(field_name, {}))
        else:
            SimpleSchema._declared_fields[field_name] = field_lookup[field_type](required=required.get(field_name, False), description=descriptions.get(field_name, ''), **kwarg_dict.get(field_name, {}))
    return SimpleSchema

def BoundCategoricalSchemaFactory(SchemaName,
                                  annotation_name,
                                  allowed_categories,
                                  required=True,
                                  category_description='',
                                  point_name='pt',
                                  category_name='category'):
    fields = {point_name: 'BoundSpatialPoint',
              category_name: 'string'}
    descriptions = {category_name: category_description,
                    point_name: 'location of object',
                    }
    required_dict = {point_name: True, category_name:required}
    validation_rules = {'categorical': [{category_name: allowed_categories}]}
    return SimpleSchemaFactory(SchemaName,
                               annotation_name,
                               fields,
                               descriptions=descriptions,
                               required=required_dict,
                               validation_rules=validation_rules)

def _validate_arguments(SchemaName, annotation_type, fields, descriptions, required, validation_rules):
    if type(SchemaName) is not str:
        raise TypeError('SchemaName must be a string')

    if type(annotation_type) is not str:
        raise TypeError('annotation_type must be a string')

    for field in fields.values():
        if field not in field_lookup:
            raise ValueError('Field {} not in valid field list'.format(field))

    for d in descriptions:
        if type(d) is not str:
            raise TypeError('All descriptions must be strings')

    for r in required.values():
        if type(r) is not bool:
            raise TypeError('Requirements must be boolean')
    for validation_rule in validation_rules:
        if validation_rule not in (validation_func_lookup):
            raise TypeError('Validation rule {} not in valid rule list'.format(validation_rule))
