import pytest
from emannotationschemas.schemas.proofreading import (
    CompartmentProofreadStatus,
    ProofreadStatus,
    ProofreadingBoolStatusUser,
)
from marshmallow import ValidationError

good_base_data = {
    "pt": {"position": [1, 2, 3]},
    "valid_id": 1234567,
    "status": "clean",
}

bad_base_data = {
    "pt": {"position": [1, 2, 3]},
    "valid_id": 1234567,
    "status": "some_nonsense",
}

good_comp_data = {
    "pt": {"position": [1, 2, 3]},
    "valid_id": 1234567,
    "status_axon": "clean",
    "status_dendrite": "extended",
}

bad_comp_data = {
    "pt": {"position": [1, 2, 3]},
    "valid_id": 1234567,
    "status_dendrite": "clean",
}

good_booluser_data = {
    "pt": {"position": [1, 2, 3]},
    "valid_id": 1234567,
    "proofread": True,
    "user_id": 42,
}

bad_booluser_data_1 = {
    "pt": {"position": [1, 2, 3]},
    "valid_id": 1234567,
    "user_id": 42,
}

bad_booluser_data_2 = {
    "pt": {"position": [1, 2, 3]},
    "valid_id": 1234567,
    "proofread": True,
}


def annotation_import(item):
    item["supervoxel_id"] = None
    item.pop("rootId", None)


def test_proofreading_validation():
    schema = ProofreadStatus(context={"bsp_fn": annotation_import})
    result = schema.load(good_base_data)
    assert result["status"] == "clean"

    with pytest.raises(ValidationError):
        schema.load(bad_base_data)


def test_compartment_proofreading_validation():
    schema = CompartmentProofreadStatus(context={"bsp_fn": annotation_import})
    result = schema.load(good_comp_data)
    assert result["status_dendrite"] == "extended"

    with pytest.raises(ValidationError):
        schema.load(bad_comp_data)


def test_bool_proofreading_user_validation_1():
    schema = ProofreadingBoolStatusUser(context={"bsp_fn": annotation_import})
    result = schema.load(good_booluser_data)
    assert result["proofread"]

    with pytest.raises(ValidationError):
        schema.load(bad_booluser_data_1)

    with pytest.raises(ValidationError):
        schema.load(bad_booluser_data_2)


def test_bool_proofreading_user_validation_2():
    schema = ProofreadingBoolStatusUser(context={"bsp_fn": annotation_import})
    result = schema.load(good_booluser_data)
    assert result["user_id"] == 42

    with pytest.raises(ValidationError):
        schema.load(bad_booluser_data_1)

    with pytest.raises(ValidationError):
        schema.load(bad_booluser_data_2)
