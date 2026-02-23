from emannotationschemas.schemas.postsynaptic_compartment import SpineWithInfo

good_spine_with_info = {
    "position": [100, 200, 300],
    "supervoxel_id": 50,
    "root_id": 10,
    "volume": 1.5,
    "n_inputs": 3,
}


def test_spine_with_info_schema():
    schema = SpineWithInfo()
    result = schema.load(good_spine_with_info)
    assert result["position"] == [100, 200, 300]
    assert result["supervoxel_id"] == 50
    assert result["root_id"] == 10
    assert result["volume"] == 1.5
    assert result["n_inputs"] == 3


def test_spine_with_info_optional():
    schema = SpineWithInfo()
    result = schema.load(
        {
            "position": [100, 200, 300],
            "supervoxel_id": 50,
            "root_id": 10,
        }
    )
    assert result["position"] == [100, 200, 300]
    assert result["supervoxel_id"] == 50
    assert result["root_id"] == 10
    assert "volume" not in result
    assert "n_inputs" not in result
