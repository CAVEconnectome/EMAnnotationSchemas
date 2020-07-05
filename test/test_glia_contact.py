from emannotationschemas.schemas.glia_contact import GliaContact

contact_size = 12.2
good_glia_contact_annotation = {
    'glia_pt': {'position': [1,2,3]},
    'object_pt': {'position': [4,5,6]},
    'size': contact_size,
    }

also_good_glia_contact_annotation = {
    'glia_pt': {'position': [1,2,3]},
    'object_pt': {'position': [4,5,6]},
    }

def annotation_import( item ):
    item['supervoxel_id'] = 5
    item.pop('rootId', None)

def test_glia_import():
    schema = GliaContact(context={'bsp_fn':annotation_import})
    result = schema.load( good_glia_contact_annotation )
    assert( result['size'] == contact_size)

    result = schema.load( also_good_glia_contact_annotation )
    assert( result['glia_pt']['supervoxel_id'] == 5)
    assert( result['object_pt']['supervoxel_id'] == 5)
