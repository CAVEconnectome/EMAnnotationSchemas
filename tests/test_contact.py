from emannotationschemas.schemas.contact import Contact

contact_data = {
    "size": 1,
    "sidea_pt": {"position": [31, 31, 0], "supervoxel_id": 95, "root_id": 4},
    "sideb_pt": {"position": [33, 33, 0], "supervoxel_id": 101, "root_id": 5},
    "ctr_pt": {"position": [4, 5, 6]},
}


def test_contact_schema():
    schema = Contact()
    result = schema.load(contact_data)
    assert result["size"] == 1
    assert result["sidea_pt"]["position"] == [31, 31, 0]
    assert result["sideb_pt"]["position"] == [33, 33, 0]
    assert result["ctr_pt"]["position"] == [4, 5, 6]
