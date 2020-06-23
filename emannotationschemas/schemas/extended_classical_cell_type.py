from emannotationschemas.schemas.categorical_factories import BoundCategoricalFactory

schema_type_name = 'extended_classical_cell_type'

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
class_name = 'ExtendedClassicalCellType'

ExtendedClassicalCellType = BoundCategoricalFactory(allowed_cell_types,
                                                    category_name,
                                                    category_description,
                                                    schema_type_name,
                                                    class_name
                                                    )
