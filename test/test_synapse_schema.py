from emannotationschemas.synapse import SynapseSchema

good_synapse = {
    'type': 'synapse',
    'pre_pt': {'position': [31, 31, 0]},
    'ctr_pt': {'position': [32, 32, 0]},
    'post_pt': {'position': [33, 33, 0]}
}

incomplete_type = {
    'pre_pt': {'position': [31, 31, 0]},
    'ctr_pt': {'position': [32, 32, 0]},
    'post_pt': {'position': [33, 33, 0]}
}
supervoxel_synapse = {
    'pre_pt': {'position': [31, 31, 0], 'supervoxel_id': 95},
    'ctr_pt': {'position': [32, 32, 0], 'supervoxel_id': 105},
    'post_pt': {'position': [33, 33, 0], 'supervoxel_id': 101}
}
supervoxel_rootId_synapse = {
    'pre_pt': {'position': [31, 31, 0], 'supervoxel_id': 95, 'rootId': 4},
    'ctr_pt': {'position': [32, 32, 0], 'supervoxel_id': 105, 'rootId': 5},
    'post_pt': {'position': [33, 33, 0], 'supervoxel_id': 101, 'rootId': 5}
}


def annotation_import(item):
    item['supervoxel_id'] = 5
    item.pop('rootId', None)


def test_synapse_validation():
    schema = SynapseSchema(context={'bsp_fn': annotation_import})
    result = schema.load(good_synapse)
    assert(result.data['pre_pt']['supervoxel_id'] == 5)

    result = schema.load(supervoxel_synapse)
    assert(result.data['pre_pt']['supervoxel_id'] == 5)

    result = schema.load(supervoxel_rootId_synapse)
    assert(result.data['pre_pt']['supervoxel_id'] == 5)
    assert('rootId' not in result.data['pre_pt'].keys())
