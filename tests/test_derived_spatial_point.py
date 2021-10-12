from emannotationschemas.schemas.derived_spatial_point import (
    DerivedNumeric,
    DerivedSpatialPoint,
    DerivedTag,
)

derived_spatial_point_data = {
    "position": [31, 31, 0],
    "supervoxel_id": 122,
    "root_id": 3232,
    "dependent_chunk": 1,
    "level": 2,
}

derived_tag_data = {
    "pt": {
        "position": [31, 31, 0],
        "supervoxel_id": 122,
        "root_id": 3232,
        "dependent_chunk": 1,
        "level": 2,
    },
    "tag": "some point",
    "valid": True,
}

derived_numeric_data = {
    "pt": {
        "position": [31, 31, 0],
        "supervoxel_id": 122,
        "root_id": 3232,
        "dependent_chunk": 1,
        "level": 2,
    },
    "value": 1.3,
    "valid": True,
}


def test_derived_spatial_point():
    schema = DerivedSpatialPoint()
    result = schema.load(derived_spatial_point_data)
    assert result["position"] == [31, 31, 0]
    assert result["supervoxel_id"] == 122
    assert result["root_id"] == 3232
    assert result["dependent_chunk"] == 1
    assert result["level"] == 2


def test_derived_tag():
    schema = DerivedTag()
    result = schema.load(derived_tag_data)

    assert result["pt"]["position"] == [31, 31, 0]
    assert result["pt"]["supervoxel_id"] == 122
    assert result["pt"]["root_id"] == 3232
    assert result["pt"]["dependent_chunk"] == 1
    assert result["pt"]["level"] == 2
    assert result["tag"] == "some point"
    assert result["valid"] == True


def test_derived_numeric():
    schema = DerivedNumeric()
    result = schema.load(derived_numeric_data)
    assert result["pt"]["position"] == [31, 31, 0]
    assert result["pt"]["supervoxel_id"] == 122
    assert result["pt"]["root_id"] == 3232
    assert result["pt"]["dependent_chunk"] == 1
    assert result["pt"]["level"] == 2
    assert result["value"] == 1.3
    assert result["valid"] == True
