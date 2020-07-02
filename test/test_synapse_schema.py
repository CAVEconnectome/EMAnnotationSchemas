from emannotationschemas.schemas.synapse import SynapseSchema
from emannotationschemas.flatten import flatten_dict
from emannotationschemas import get_flat_schema
import pytest
import marshmallow as mm

good_synapse = {
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
    'ctr_pt': {'position': [32, 32, 0]},
    'post_pt': {'position': [33, 33, 0], 'supervoxel_id': 101}
}
supervoxel_rootId_synapse = {
    'pre_pt': {'position': [31, 31, 0], 'supervoxel_id': 95, 'root_id': 4},
    'ctr_pt': {'position': [32, 32, 0]},
    'post_pt': {'position': [33, 33, 0], 'supervoxel_id': 101, 'root_id': 5}
}

supervoxel_rootId_invalid_synapse = {
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
    assert(result['pre_pt']['supervoxel_id'] == 5)
    schema.validate(result)

    result = schema.load(supervoxel_synapse)
    assert(result['pre_pt']['supervoxel_id'] == 5)

    result = schema.load(supervoxel_rootId_synapse)
    assert(result['pre_pt']['supervoxel_id'] == 5)
    assert('rootId' not in result['pre_pt'].keys())


def test_synapse_flatten():
    schema = SynapseSchema()
    result = schema.load(good_synapse)
    d = flatten_dict(result)
    print(d)
    assert(d['pre_pt_position'] == [31, 31, 0])

    result = schema.load(supervoxel_synapse)
    assert(d['pre_pt_position'] == [31, 31, 0])

    result = schema.load(supervoxel_rootId_synapse)
    assert(d['pre_pt_position'] == [31, 31, 0])

    FlatSynapseSchema = get_flat_schema('synapse')
    schema = FlatSynapseSchema()
    result = schema.load(d)
    
    assert(len(result) == 9)


def test_synapse_postgis():
    schema = SynapseSchema(context={'postgis': True})
    result = schema.load(good_synapse)
    d = flatten_dict(result)
    assert(d['pre_pt_position'] == 'POINTZ(31 31 0)')


def test_synapse_validity():
    schema = SynapseSchema()
    result = schema.load(supervoxel_rootId_synapse)
    print('valid test', result)
    assert result['valid']
    result = schema.load(good_synapse)
    


def test_synapse_invalid():
    schema = SynapseSchema()
    with pytest.raises(mm.ValidationError):
        result = schema.load(supervoxel_rootId_invalid_synapse)

