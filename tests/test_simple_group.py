from emannotationschemas.schemas.groups import SimpleGroup, SimpleGroupIndexed

good_simple_group = {
    "pt": {"position": [31, 32, 33]},
    "group_id": 42,
    "target_id": 456,
}

good_simple_group_indexed = {
    "pt": {"position": [10, 20, 30]},
    "group_id": 123,
    "target_id": 456,
}


def test_simple_group_schema():
    schema = SimpleGroup()
    result = schema.load(good_simple_group)
    assert result["group_id"] == 42
    assert result["pt"]["position"] == [31, 32, 33]


def test_simple_group_indexed_schema():
    schema = SimpleGroupIndexed()
    result = schema.load(good_simple_group_indexed)
    assert result["group_id"] == 123
    assert result["pt"]["position"] == [10, 20, 30]
