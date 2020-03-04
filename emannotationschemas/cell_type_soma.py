from emannotationschemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm
from marshmallow.validate import OneOf

allowed_level_one = ['excitatory',
                     'inhibitory',
                     'glia',
                     'uncertain_class']

allowed_types = dict(
                    excitatory=['PL5',
                                'PL23',
                                'PL4',
                                'PL6',
                                'uncertain_type'],
                    inhibitory=['chandelier',
                               'martinotti',
                               'pv',
                               'sst',
                               'vip',
                               'basket',
                               'neurogliaform',
                             
                               'uncertain_type'],
                    glia = [  'astrocyte',
                               'microglia',
                               'OPC',
                               'oligodendrocyte',
                               'uncertain'],
                    uncertain_class=[]
                    )


class CellTypeSoma(AnnotationSchema):

    level_one = mm.fields.String(
                            required=True,
                            description='Classification system followed',
                            validate=OneOf(allowed_level_one))
    level_two = mm.fields.String(
                            required=True,
                            description='Cell type name')
    pt = mm.fields.Nested( BoundSpatialPoint, 
                            required=True,
                            description='Location associated with classification')
    @mm.post_load
    def validate_type( self, item):
        system = item['level_one']
        if system in allowed_types.keys():
            if item['level_two'] not in allowed_types[system]:
                item['valid'] = False
            else:
                item['valid'] = True
        else:
            item['valid'] = True

        return item