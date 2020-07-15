from emannotationschemas.cell_type_local import Soma

good_soma = {
    'type' : 'soma',
    'ctr_pt':{'position' : [1,2,3]},
    }

volume = 1.0
nucleus = 123
synapses = 10

also_good_soma = {
    'type' : 'soma',
    'ctr_pt':{'position' : [1,2,3]},
    'volume': volume,
    'nucleus': nucleus,
    'soma_synapses' = synapses
    }

def annotation_import( item ):
    item['supervoxel_id'] = 5
    item.pop('rootId', None)

def test_soma_validation():
    schema = Soma(context={'bsp_fn':annotation_import})
    result = schema.load( good_soma )
    assert( result.data['ctr_pt']['supervoxel_id'] == 5)
    assert result.data['valid']

    result = schema.load( also_good_soma )
    assert( result.data['ctr_pt']['supervoxel_id'] == 5)
    assert( result.data['volume'] == volume)
    assert( result.data['nucleus'] == nucleus)
    assert( result.data['soma_synapses'] == synapses)