from emannotationschemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm
from marshmallow.validate import OneOf

allowed_classification_systems = ['ivscc_m',
                             'valence',
                             'classical',
                             ]

allowed_types = dict(
                    valence=['e',
                             'i',
                             'g',
                             'uncertain'],
                    ivscc_m=['spiny_{}'.format(i) for i in range(1, 15)] +
                            ['aspiny_s_{}'.format(i) for i in range(1, 17)] +
                            ['aspiny_d_{}'.format(i) for i in range(1, 6)] +
                            ['uncertain'],

                    classical=['chandelier',
                               'pyramidal',
                               'martinotti',
                               'pv',
                               'sst',
                               'vip',
                               'clutch',
                               'ivy',
                               'basket',
                               'neurogliaform',
                               'astrocyte',
                               'microglia-perivascular',
                               'microglia-perineuronal',
                               'uncertain',
                               ]
                    )


class CellTypeLocal(AnnotationSchema):

    classification_system = mm.fields.String(
                            required=True,
                            description='Classification system followed',
                            validate=OneOf(allowed_classification_systems))
    cell_type = mm.fields.String(
                            required=True,
                            description='Cell type name')
    pt = mm.fields.Nested( BoundSpatialPoint, 
                            required=True,
                            description='Location associated with classification')
    @mm.post_load
    def validate_type( self, item):
        assert item['type'] == 'cell_type_local'

        system = item['classification_system']
        if system in allowed_types.keys():
            if item['cell_type'] not in allowed_types[system]:
                item['valid'] = False
            else:
                item['valid'] = True
        else:
            item['valid'] = True

        return item