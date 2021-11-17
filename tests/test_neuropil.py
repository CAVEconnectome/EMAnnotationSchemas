from emannotationschemas.schemas.neuropil import FlyNeuropil


good_neuropil = [
    {
        "target_id": 1,
        "neuropil": "foo",
    }
]


def test_neuropil_type_schema():
    schema = FlyNeuropil()
    results = schema.load(good_neuropil, many=True)
    for index, result in enumerate(results):
        assert result["target_id"] == good_neuropil[index]["target_id"]
        assert result["neuropil"] == good_neuropil[index]["neuropil"]
