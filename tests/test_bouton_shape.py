import pytest
from emannotationschemas.schemas.bouton_shape import BoutonShape


good_bouton_shapes = [
    {
        "target_id": 1,
        "shape": "pancake",
    },
    {
        "target_id": 2,
        "shape": "basmati",
    },
    {
        "target_id": 3,
        "shape": "potato",
    },
]

bad_bouton_shape = {
    "target_id": 4,
    "shape": "hotdog",
}


def test_bouton_shape_schema():
    schema = BoutonShape()
    results = schema.load(good_bouton_shapes, many=True)
    for index, result in enumerate(results):
        assert result["target_id"] == good_bouton_shapes[index]["target_id"]
        assert result["shape"] == good_bouton_shapes[index]["shape"]


def test_bad_bouton_shape():
    with pytest.raises(Exception) as excinfo:
        schema = BoutonShape()
        result = schema.load(bad_bouton_shape)
        assert "{'shape': ['Must be one of: pancake, basmati, potato.']}" in str(
            excinfo.value
        )
