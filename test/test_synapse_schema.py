from emannotationschemas.synapse import SynapseSchema
from emannotationschemas.base import flatten_dict
from emannotationschemas import get_flat_schema


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
    'type': 'synapse',
    'pre_pt': {'position': [31, 31, 0], 'supervoxel_id': 95},
    'ctr_pt': {'position': [32, 32, 0], 'supervoxel_id': 105},
    'post_pt': {'position': [33, 33, 0], 'supervoxel_id': 101}
}
supervoxel_rootId_synapse = {
    'type': 'synapse',
    'pre_pt': {'position': [31, 31, 0], 'supervoxel_id': 95, 'root_id': 4},
    'ctr_pt': {'position': [32, 32, 0], 'supervoxel_id': 105, 'root_id': 5},
    'post_pt': {'position': [33, 33, 0], 'supervoxel_id': 101, 'root_id': 5}
}

supervoxel_rootId_invalid_synapse = {
    'type': 'synapse',
    'pre_pt': {'position': [31, 31, 0], 'supervoxel_id': 95, 'root_id': 5},
    'ctr_pt': {'position': [32, 32, 0], 'supervoxel_id': 105, 'root_id': 5},
    'post_pt': {'position': [33, 33, 0], 'supervoxel_id': 101, 'root_id': 5}
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


def test_synapse_flatten():
    schema = SynapseSchema()
    result = schema.load(good_synapse)
    d = flatten_dict(result.data)
    print(d)
    assert(d['pre_pt_position'] == [31, 31, 0])

    result = schema.load(supervoxel_synapse)
    assert(d['pre_pt_position'] == [31, 31, 0])

    result = schema.load(supervoxel_rootId_synapse)
    assert(d['pre_pt_position'] == [31, 31, 0])

    FlatSynapseSchema = get_flat_schema('synapse')
    schema = FlatSynapseSchema()
    result = schema.load(d)
    assert(len(result.errors) == 0)


def test_synapse_postgis():
    schema = SynapseSchema(context={'postgis': True})
    result = schema.load(good_synapse)
    d = flatten_dict(result.data)
    assert(d['pre_pt_position'] == 'POINTZ(31 31 0)')


def test_synapse_validity():
    schema = SynapseSchema()
    result = schema.load(supervoxel_rootId_synapse)
    print('valid test', result.data)
    assert result.data['valid']
    result = schema.load(good_synapse)
    assert 'valid' not in result.data.keys()


def test_synapse_invalid():
    schema = SynapseSchema()
    result = schema.load(supervoxel_rootId_invalid_synapse)
    print('test', result.data, result.errors)
    assert not result.data['valid']
