from emannotationschemas.schemas.neuropil import NeuropilType


good_neuropil_type = [
    {
        "target_id": 1,
        "neuropil": "foo",
    }
]


def test_neuropil_type_schema():
    schema = NeuropilType()
    results = schema.load(good_neuropil_type, many=True)
    for index, result in enumerate(results):
        assert result["target_id"] == good_neuropil_type[index]["target_id"]
        assert result["neuropil"] == good_neuropil_type[index]["neuropil"]
