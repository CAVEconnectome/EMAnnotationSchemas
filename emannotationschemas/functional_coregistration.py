# from emannotationschemas.base import BoundSpatialPoint, \
#     AnnotationSchema
# import marshmallow as mm

from emannotationschemas.schema_factory import SimpleSchemaFactory
FunctionalCoregistration = SimpleSchemaFactory('FunctionalCoregistration',
                                               'microns_func_coreg',
                                               fields={'pt': 'BoundSpatialPoint', 'func_id': 'int'},
                                               descriptions={'pt': 'location of cell body of functional cell',
                                                             'func_id': 'functional cell ID'},
                                               required={'pt': True, 'func_id':True})

# class FunctionalCoregistration(AnnotationSchema):
#     pt = mm.fields.Nested(BoundSpatialPoint, required=True,
#                           description="location of cell body of functional cell")
#     func_id = mm.fields.Int(required=True, description="functional cell ID")

#     @mm.post_load
#     def validate_type(self, item):
#         # check that the annotation type is present in the object as 'functional_coregistration'
#         assert item['type'] == 'microns_func_coreg'
