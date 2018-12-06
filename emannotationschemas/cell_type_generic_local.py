from emannotationschemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm
from marshmallow.validate import OneOf

class BoundTagAnnotation(AnnotationSchema):
    pt = mm.fields.Nested(BoundSpatialPoint,
                         required=True,
                         description='Location associated with the tag')
    tag = mm.fields.String(required=true,
                           description='Arbitrary text tag')
    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == 'bound_tag'
        return item


def BoundCategoricalFactory(allowed_categories):
    class BoundCategoricalAnnotation(AnnotationSchema):
        pt = mm.fields.Nested(BoundSpatialPoint,
                             required=True,
                             description='Location associated with the tag')
        category = mm.fields.String(required=true,
                                    description='Categorical text tag')
        
        @mm.post_load
        def validate_type(self, item):
            assert item['type'] == 'bound_categorical'
            if item['category'] in allowed_categories:
                item['valid'] = True
            else:
                item['valid'] = False
            return item
    return BoundCategoricalAnnotation


def BoundCategoricalSystemFactory(classification_system, allowed_category_dict):
    class BoundClassificationSystemAnnotation(AnnotationSchema):
        pt = mm.fields.Nested(BoundSpatialPoint,
                     required=True,
                     description='Location associated with the tag')
        category = mm.fields.String(required=true,
                                    description='Categorical text tag')
        classification_system = mm.fields.String(required=true,
                                    description='Classification system for cateogory')

        @mm.post_load
        def validate_type(self, item):
            assert item['type'] == 'bound_categorical_system'
            if item['category'] in allowed_category_dict[item['classification_system']]:
                item['valid'] = True
            else:
                item['valid'] = False
            return item
    return BoundClassificationSystemAnnotation