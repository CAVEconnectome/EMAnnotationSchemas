from emannotationschemas.tags import BoundTagAnnotation, ReferenceTagAnnotation

reference_tag= {
    'type': 'reference_tag',
    'tag' : "This tag points at an object",
    'target_id': 98109,
    'reference_type': 'any'
}

bound_tag = {
    'type': 'bound_tag',
    'tag': 'This tag points to a location in space',
    'pt': {'position': [1,2,3]}
}

def annotation_import(item):
    item['supervoxel_id'] = 5
    item.pop('rootId', None)

def test_reference_tag():
    schema = ReferenceTagAnnotation()
    result = schema.load( reference_tag )
    assert( result.data['tag'][-6:] == 'object' )

def test_bound_tag():
    schema = BoundTagAnnotation(context={'bsp_fn':annotation_import})
    result = schema.load( bound_tag )
    assert( result.data['pt']['supervoxel_id'] == 5)