from emannotationschemas.schemas.extended_classical_cell_type import ExtendedClassicalCellType

good_cell_type = {
    'cell_type':'vip-chat',
    'pt': {'position' : [1,2,3]}
    }

bad_cell_type = {
    'cell_type':'fake_cell_type',
    'pt': {'position' : [1,2,3]}
    }

def annotation_import( item ):
    item['supervoxel_id'] = 5
    item.pop('rootId', None)

def test_cell_type_validation():
    schema = ExtendedClassicalCellType(context={'bsp_fn':annotation_import})
    result = schema.load( good_cell_type )
    assert( result['pt']['supervoxel_id'] == 5)
    assert result['valid']

def test_cell_type_invalid():
    schema = ExtendedClassicalCellType(context={'bsp_fn':annotation_import})
    result = schema.load( bad_cell_type )
    assert not result['valid']