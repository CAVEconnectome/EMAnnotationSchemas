from emannotationschemas.schemas.fly_cell_types import FlyCellType, FlyCellTypeExt
import pytest
import marshmallow as mm

good_fly_cell_type = {
    "hemisphere": "L",
    "cell_type": "fly_1",
    "pt": {"position": [1, 2, 3]},
}

good_fly_cell_type_1_ext = good_fly_cell_type.copy()
good_fly_cell_type_1_ext["synonym"] = "GrayWhale"
good_fly_cell_type_1_ext["driver_line"] = "DrivingInTheRain"

good_fly_cell_type_2_ext = good_fly_cell_type.copy()

bad_fly_cell_type = {
    "hemisphere": "O",
    "cell_type": "fly_1",
    "pt": {"position": [1, 2, 3]},
}


def annotation_import(item):
    item["supervoxel_id"] = 5
    item.pop("rootId", None)


def test_fly_cell_type():
    schema = FlyCellType(context={"bsp_fn": annotation_import})
    result = schema.load(good_fly_cell_type)
    assert result["pt"]["supervoxel_id"] == 5


def test_fly_cell_type_ext():
    schema = FlyCellTypeExt(context={"bsp_fn": annotation_import})
    result = schema.load(good_fly_cell_type_1_ext)
    assert result["pt"]["supervoxel_id"] == 5

    schema = FlyCellTypeExt(context={"bsp_fn": annotation_import})
    result = schema.load(good_fly_cell_type_2_ext)
    assert result["pt"]["supervoxel_id"] == 5


def test_bad_cell_type():
    schema = FlyCellType()
    with pytest.raises(mm.ValidationError):
        result = schema.load(bad_fly_cell_type)
