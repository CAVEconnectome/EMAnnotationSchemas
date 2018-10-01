from emannotationschemas.cell_type_local import CellTypeLocal

good_ivscc_cell_type = {
    'type' : 'cell_type_local',
    'classification_system': 'ivscc_m',
    'cell_type':'spiny_4',
    'pt': {'position' : [1,2,3]}
    }

bad_classical_cell_type = {
    'type' : 'cell_type_local',
    'classification_system': 'classical',
    'cell_type':'spiny_4',
    'pt': {'position' : [5,2,3]}
    }

def annotation_import( item ):
    item['supervoxel_id'] = 5
    item.pop('rootId', None)

def test_cell_type_validation():
    schema = CellTypeLocal(context={'bsp_fn':annotation_import})
    result = schema.load( good_ivscc_cell_type )
    assert( result.data['pt']['supervoxel_id'] == 5)

def test_cell_type_invalid():
    schema = CellTypeLocal(context={'bsp_fn':annotation_import})
    result = schema.load( bad_classical_cell_type )
    assert not result.data['valid']