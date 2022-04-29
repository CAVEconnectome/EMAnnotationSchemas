from emannotationschemas.schemas.nucleus_detection import NucleusDetection


good_nucleus_detection_data = {
    "target_id": 1,
    "pt": {"position": [1, 2, 3]},
    "volume": 3.0,
    "bb_start": {"position": [1, 2, 3]},
    "bb_end": {"position": [4, 5, 6]}
}


def test_nucleus_schema():
    schema = NucleusDetection()
    result = schema.load(good_nucleus_detection_data)
    assert result["target_id"] == 1
    assert result["pt"]["position"] == [1, 2, 3]
    assert result["volume"] == 3.0
    assert result["bb_start"]["position"] == [1, 2, 3]
    assert result["bb_end"]["position"] == [4, 5, 6]
