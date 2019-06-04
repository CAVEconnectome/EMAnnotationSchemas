# from emannotationschemas.categorical_factories import BoundCategoricalFactory
from emannotationschemas.schema_factory import BoundCategoricalSchemaFactory

annotation_name = 'extended_classical_cell_type'

allowed_cell_types = ['basket',
                      'chandelier',
                      'oligodendrocyte',
                      'vip-i',
                      'martinotti',
                      'neurogliaform',
                      'vip-chat',
                      'vip-apical',
                      'ivy',
                      'clutch',
                      'sst',
                      'pyramidal',
                      'uncertain'
                      ]

category_name = 'cell_type'
category_description = 'cell type name'
SchemaName = 'ExtendedClassicalCellType'

ExtendedClassicalCellType = BoundCategoricalSchemaFactory(SchemaName,
                                                          annotation_name,
                                                          allowed_cell_types,
                                                          category_name = 'cell_type',
                                                          category_description=category_description,
                                                          )