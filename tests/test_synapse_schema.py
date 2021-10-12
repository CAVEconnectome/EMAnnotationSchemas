import marshmallow as mm
import pytest
from emannotationschemas import get_flat_schema
from emannotationschemas.flatten import flatten_dict
from emannotationschemas.schemas.synapse import (
    BaseSynapseSchema,
    BuhmannEcksteinSynapseSchema,
    BuhmannSynapseSchema,
    NoCleftSynapse,
    PlasticSynapse,
    SynapseSchema,
)

good_base_synapse = {
    "pre_pt": {"position": [31, 31, 0], "supervoxel_id": 95, "root_id": 4},
    "post_pt": {"position": [33, 33, 0], "supervoxel_id": 101, "root_id": 5},
}


good_no_cleft_synapse = {
    'pre_pt': {'position': [31, 31, 0], 'supervoxel_id': 95, 'root_id': 4},
    'post_pt': {'position': [33, 33, 0], 'supervoxel_id': 101, 'root_id': 5},
    'score': 50
}

good_synapse = {
    "pre_pt": {"position": [31, 31, 0]},
    "ctr_pt": {"position": [32, 32, 0]},
    "post_pt": {"position": [33, 33, 0]},
}

incomplete_type = {
    "pre_pt": {"position": [31, 31, 0]},
    "ctr_pt": {"position": [32, 32, 0]},
    "post_pt": {"position": [33, 33, 0]},
}
supervoxel_synapse = {
    "pre_pt": {"position": [31, 31, 0], "supervoxel_id": 95},
    "ctr_pt": {"position": [32, 32, 0]},
    "post_pt": {"position": [33, 33, 0], "supervoxel_id": 101},
}
supervoxel_rootId_synapse = {
    "pre_pt": {"position": [31, 31, 0], "supervoxel_id": 95, "root_id": 4},
    "ctr_pt": {"position": [32, 32, 0]},
    "post_pt": {"position": [33, 33, 0], "supervoxel_id": 101, "root_id": 5},
}

supervoxel_rootId_invalid_synapse = {
    "pre_pt": {"position": [31, 31, 0], "supervoxel_id": 95, "root_id": 5},
    "ctr_pt": {"position": [32, 32, 0], "supervoxel_id": 105, "root_id": 5},
    "post_pt": {"position": [33, 33, 0], "supervoxel_id": 101, "root_id": 5},
}


good_buhmann_synapse = {
    "pre_pt": {"position": [31, 31, 0], "supervoxel_id": 95, "root_id": 4},
    "post_pt": {"position": [33, 33, 0], "supervoxel_id": 101, "root_id": 5},
    "connection_score": 1.32,
    "cleft_score": 1.0,
}

good_buhmann_eckstein_synapse = {
    "pre_pt": {"position": [31, 31, 0], "supervoxel_id": 95, "root_id": 4},
    "post_pt": {"position": [33, 33, 0], "supervoxel_id": 101, "root_id": 5},
    "connection_score": 1.32,
    "cleft_score": 1.0,
    "gaba": 0.8,
    "ach": 0.0,
    "glut": 0.1,
    "oct": 0.1,
    "ser": 0.0,
    "da": 0.2,
    "valid_nt": True,
}

good_plastic_synapse = {
    "pre_pt": {"position": [31, 31, 0]},
    "ctr_pt": {"position": [32, 32, 0]},
    "post_pt": {"position": [33, 33, 0]},
    "plasticity": 1,
}

# class PlasticSynapse(SynapseSchema):
#     plasticity = mm.fields.Int(required=True,
#                                validate=mm.validate.OneOf([0, 1, 2, 3, 4]),
#                                description="plasticity state 0:not synapse 1:normal 2:mild 3:strong 4:not rated")


def annotation_import(item):
    item["supervoxel_id"] = 5
    item.pop("rootId", None)


def test_base_synapse_schema():
    schema = BaseSynapseSchema()
    result = schema.load(good_base_synapse)
    assert result["pre_pt"]["position"] == [31, 31, 0]
    assert result["pre_pt"]["supervoxel_id"] == 95
    assert result["pre_pt"]["root_id"] == 4
    assert result["post_pt"]["position"] == [33, 33, 0]
    assert result["post_pt"]["supervoxel_id"] == 101
    assert result["post_pt"]["root_id"] == 5

    assert "rootId" not in result["pre_pt"].keys()


def test_no_cleft_synapse_schema():
    schema = NoCleftSynapse()
    result = schema.load(good_no_cleft_synapse)
    assert result["pre_pt"]["position"] == [31, 31, 0]
    assert result["pre_pt"]["supervoxel_id"] == 95
    assert result["pre_pt"]["root_id"] == 4
    assert result["post_pt"]["position"] == [33, 33, 0]
    assert result["post_pt"]["supervoxel_id"] == 101
    assert result["post_pt"]["root_id"] == 5
    assert result["score"] == 50.0
    assert "rootId" not in result["pre_pt"].keys()


def test_buhmann_synapse_schema():
    schema = BuhmannSynapseSchema()
    result = schema.load(good_buhmann_synapse)
    assert result["pre_pt"]["position"] == [31, 31, 0]
    assert result["pre_pt"]["supervoxel_id"] == 95
    assert result["cleft_score"] == 1.0
    assert result["connection_score"] == 1.32

    assert "rootId" not in result["pre_pt"].keys()


def test_buhmann_eckstein_synapse_schema():
    schema = BuhmannEcksteinSynapseSchema()
    result = schema.load(good_buhmann_eckstein_synapse)
    assert result["pre_pt"]["position"] == [31, 31, 0]
    assert result["pre_pt"]["supervoxel_id"] == 95
    assert result["cleft_score"] == 1.0
    assert result["gaba"] == 0.8
    assert result["ach"] == 0.0
    assert result["glut"] == 0.1
    assert result["oct"] == 0.1
    assert result["ser"] == 0.0
    assert result["da"] == 0.2
    assert result["valid_nt"] == True
    assert "rootId" not in result["pre_pt"].keys()


def test_synapse_validation():
    schema = SynapseSchema(context={"bsp_fn": annotation_import})
    result = schema.load(good_synapse)
    assert result["pre_pt"]["supervoxel_id"] == 5
    schema.validate(result)

    result = schema.load(supervoxel_synapse)
    assert result["pre_pt"]["supervoxel_id"] == 5

    result = schema.load(supervoxel_rootId_synapse)
    assert result["pre_pt"]["supervoxel_id"] == 5
    assert "rootId" not in result["pre_pt"].keys()


def test_plastic_synapse_schema():
    schema = PlasticSynapse()
    result = schema.load(good_plastic_synapse)
    assert result["plasticity"] == 1


def test_synapse_flatten():
    schema = SynapseSchema()
    result = schema.load(good_synapse)
    d = flatten_dict(result)

    assert d["pre_pt_position"] == [31, 31, 0]

    result = schema.load(supervoxel_synapse)
    assert d["pre_pt_position"] == [31, 31, 0]

    result = schema.load(supervoxel_rootId_synapse)
    assert d["pre_pt_position"] == [31, 31, 0]

    FlatSynapseSchema = get_flat_schema("synapse")
    schema = FlatSynapseSchema()
    result = schema.load(d)

    assert len(result) == 8


def test_synapse_postgis():
    schema = SynapseSchema(context={"postgis": True})
    result = schema.load(good_synapse)
    d = flatten_dict(result)
    assert d["pre_pt_position"] == "POINTZ(31 31 0)"


def test_synapse_validity():
    schema = SynapseSchema()
    result = schema.load(supervoxel_rootId_synapse)
    print("valid test", result)
    assert result["valid"]
    result = schema.load(good_synapse)


def test_synapse_invalid():
    schema = SynapseSchema()
    with pytest.raises(mm.ValidationError):
        result = schema.load(supervoxel_rootId_invalid_synapse)
