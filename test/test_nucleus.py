from emannotationschemas.cell_type_local import Nucleus

good_nucleus = {
    'type' : 'nucleus',
    'ctr_pt':{'position' : [1,2,3]},
    }

volume = 1.0
cell = 123

also_good_nucleus = {
    'type' : 'nucleus',
    'ctr_pt':{'position' : [1,2,3]},
    'volume': volume,
    'cell_body': cell
    }

def annotation_import( item ):
    item['supervoxel_id'] = 5
    item.pop('rootId', None)

def test_nucleus_validation():
    schema = Nucleus(context={'bsp_fn':annotation_import})
    result = schema.load( good_nucleus )
    assert( result.data['ctr_pt']['supervoxel_id'] == 5)
    assert result.data['valid']

    result = schema.load( also_good_nucleus )
    assert( result.data['ctr_pt']['supervoxel_id'] == 5)
    assert( result.data['volume'] == volume)
    assert( result.data['cell_body'] == cell)