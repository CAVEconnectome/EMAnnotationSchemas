from emannotationschemas.tags import BoundTagAnnotation, TypedReferenceTags

synapse_reference_tag_data = {
    'type': 'synapse_reference_tag',
    'tag' : "This tag points at a synapse",
    'target_id': 98109,
    'reference_type': 'synapse_reference_tag'
}

reference_tag_reference_tag_data = {
    'type': 'reference_tag_reference_tag',
    'tag' : "This tag points at a reference tag",
    'target_id': 98109,
    'reference_type': 'reference_tag_reference_tag'
}

bound_tag = {
    'type': 'bound_tag',
    'tag': 'This tag points to a location in space',
    'pt': {'position': [1,2,3]}
}

def annotation_import(item):
    item['supervoxel_id'] = 5
    item.pop('rootId', None)

def test_bound_tag():
    schema = BoundTagAnnotation(context={'bsp_fn':annotation_import})
    result = schema.load( bound_tag )
    assert result.data['pt']['supervoxel_id'] == 5

def test_proper_reference_tag():
    schema = TypedReferenceTags['synapse']()
    result = schema.load( synapse_reference_tag_data )
    assert result.data['tag'][-7:] == 'synapse' 

    schema = TypedReferenceTags['reference_tag']()
    result = schema.load( reference_tag_reference_tag_data )
    assert result.data['tag'][-3:] == 'tag' 

def test_improper_reference_tag():
    schema = TypedReferenceTags['synapse']()
    try:
        result = schema.load( reference_tag_reference_tag_data )
    except AssertionError:
        assert True
