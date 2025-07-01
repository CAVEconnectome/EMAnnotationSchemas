import logging

from emannotationschemas import get_flat_schema
from emannotationschemas.schemas.nucleus_detection import NucleusDetection

good_nucleus_detection_data = {
    "target_id": 1,
    "pt": {"position": [1, 2, 3]},
    "volume": 3.0,
    "bb_start": {"position": [1, 2, 3]},
    "bb_end": {"position": [4, 5, 6]}
}

nuclues_data_without_bb = {
    "target_id": 1,
    "pt": {"position": [1, 2, 3]},
    "volume": 3.0,
    "bb_start": None,
    "bb_end": None
}


def test_nucleus_schema():
    schema = NucleusDetection()
    result = schema.load(good_nucleus_detection_data)
    assert result["target_id"] == 1
    assert result["pt"]["position"] == [1, 2, 3]
    assert result["volume"] == 3.0
    assert result["bb_start"]["position"] == [1, 2, 3]
    assert result["bb_end"]["position"] == [4, 5, 6]

def test_nucleus_schema_without_bb():
    schema = NucleusDetection()
    result = schema.load(nuclues_data_without_bb)
    assert result["target_id"] == 1
    assert result["pt"]["position"] == [1, 2, 3]
    assert result["volume"] == 3.0
    assert result["bb_start"] is None
    assert result["bb_end"] is None

def test_flattend_schema():

    FlatSchema = get_flat_schema("nucleus_detection")
    flat_schema = FlatSchema()
    
    assert flat_schema.fields['pt_position'].required == True
    
    assert flat_schema.fields['bb_start_position'].required == False
    assert flat_schema.fields['bb_end_position'].required == False
    
    for field_name, field in flat_schema.fields.items():
        logging.info(f"{field_name}: required={field.required}")

    