from emannotationschemas.schemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm

def BoundCategoricalFactory(allowed_categories,
                            category_name,
                            category_description,
                            schema_type_name,
                            class_name=None):
    class BoundCategoricalAnnotation(AnnotationSchema):
        pt = mm.fields.Nested(BoundSpatialPoint,
                              required=True,
                              description='Location in space')

        @mm.post_load
        def validate_type(self, item, **kwargs):
            if item[category_name] in allowed_categories:
                item['valid'] = True
            else:
                item['valid'] = False
            return item

    BoundCategoricalAnnotation._declared_fields[category_name] = mm.fields.String(required=True, description=category_description)
    if class_name is not None:
        BoundCategoricalAnnotation.__name__ = class_name
    return BoundCategoricalAnnotation

def BoundCategoricalSystemFactory(allowed_category_dict,
                                  category_name,
                                  category_description,
                                  schema_type_name,
                                  class_name=None):
    class BoundClassificationSystemAnnotation(AnnotationSchema):
        pt = mm.fields.Nested(BoundSpatialPoint,
                     required=True,
                     description='Location in space')
        classification_system = mm.fields.String(required=True,
                                    description='Classification system used')

        @mm.post_load
        def validate_type(self, item, **kwargs):
            if item[category_name] in allowed_category_dict[item['classification_system']]:
                item['valid'] = True
            else:
                item['valid'] = False
            return item
    BoundClassificationSystemAnnotation._declared_fields[category_name] = mm.fields.String(required=True, description=category_description)
    if class_name is not None:
        BoundClassificationSystemAnnotation.__name__ = class_name

    return BoundClassificationSystemAnnotation