import marshmallow as mm
import pytest
from emannotationschemas.models import (
    Base,
    UnknownAnnotationTypeException,
    make_model_from_schema,
    make_flat_model,
    make_dataset_models,
    make_segmentation_model,
    make_annotation_model,
    format_database_name,
    format_version_db_uri,
)


def test_format_database_name():
    formatted_name = format_database_name("test_aligned_volume", 1)
    assert formatted_name == "test_aligned_volume_v1"


def test_format_version_db_uri():
    sql_uri = "postgres://postgres:test@localhost:5432/test"
    formatted_db_name = format_version_db_uri(sql_uri, "test_aligned_volume", 1)
    assert (
        formatted_db_name
        == "postgres://postgres:test@localhost:5432/test_aligned_volume_v1"
    )


def test_model_creation():
    metadata_dict = {"spinecall": {"reference_table": "synapse"}}
    model_dict = make_dataset_models(
        aligned_volume="test",
        schemas_and_tables=[
            ("synapse", "synapse"),
            ("postsynaptic_compartment", "spinecall"),
        ],
        include_contacts=True,
        segmentation_source=None,
        metadata_dict=metadata_dict,
        with_crud_columns=True,
    )
    check_model_dict(model_dict, "synapse", "synapse")
    check_model_dict(model_dict, "contact", "test__contact")
    check_model_dict(model_dict, "spinecall", "spinecall")


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_make_annotation_model():
    import warnings

    with warnings.catch_warnings(record=True) as w:
        model = make_annotation_model("test_synapses", "synapse")
    assert model.__name__ == "test_synapses"

    columns = [
        "id",
        "created",
        "deleted",
        "superceded_id",
        "valid",
        "pre_pt_position",
        "post_pt_position",
        "ctr_pt_position",
        "size",
    ]
    model_columns = [column.name for column in model.__table__.columns]
    assert model_columns == columns


def test_make_model_annotation_from_schema():
    model = make_model_from_schema("test_synapses", "synapse")
    assert model.__name__ == "test_synapses"

    columns = [
        "id",
        "created",
        "deleted",
        "superceded_id",
        "valid",
        "pre_pt_position",
        "post_pt_position",
        "ctr_pt_position",
        "size",
    ]
    model_columns = [column.name for column in model.__table__.columns]
    assert model_columns == columns


def test_cache_not_updating():
    model = make_model_from_schema("test_synapses", "synapse", with_crud_columns=False)
    is_crud_col = [col.name for col in model.__table__.columns if col.name == "created"]
    assert is_crud_col[0] == "created"


def test_reset_cache_update():
    model = make_model_from_schema(
        "test_synapses", "synapse", with_crud_columns=False, reset_cache=True
    )
    is_crud_col = [col.name for col in model.__table__.columns if col.name == "created"]
    assert not is_crud_col


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_make_segmentation_model():
    import warnings

    with warnings.catch_warnings(record=True) as w:
        model = make_segmentation_model(
            "test_synapses", "synapse", "test_pcg", with_crud_columns=False
        )
    assert model.__name__ == "test_synapses__test_pcg"

    columns = [
        "id",
        "pre_pt_supervoxel_id",
        "pre_pt_root_id",
        "post_pt_supervoxel_id",
        "post_pt_root_id",
    ]
    model_columns = [column.name for column in model.__table__.columns]
    assert model_columns == columns


def test_make_model_segmentation_from_schema():
    model = make_model_from_schema(
        "test_synapses", "synapse", "test_pcg", with_crud_columns=False
    )
    assert model.__name__ == "test_synapses__test_pcg"

    columns = [
        "id",
        "pre_pt_supervoxel_id",
        "pre_pt_root_id",
        "post_pt_supervoxel_id",
        "post_pt_root_id",
    ]
    model_columns = [column.name for column in model.__table__.columns]
    assert model_columns == columns


def test_make_flat_model():
    model = make_flat_model("flat_synapses", "synapse", "test_pcg")
    assert model.__name__ == "flat_synapses"
    columns = [
        "id",
        "valid",
        "pre_pt_position",
        "pre_pt_supervoxel_id",
        "pre_pt_root_id",
        "post_pt_position",
        "post_pt_supervoxel_id",
        "post_pt_root_id",
        "ctr_pt_position",
        "size",
    ]
    model_columns = [column.name for column in model.__table__.columns]
    assert model_columns == columns


def check_model_dict(model_dict, schema_type, table_name):
    synapse_model = model_dict[schema_type]
    assert synapse_model.__name__ == table_name
    assert issubclass(synapse_model, Base)


def test_wrong_reference_schmea():
    """Check that non-reference schema skips
    reference schema columns during model creation when
    optional metadata dict is passed with a reference"""
    table_args = {
        "table_name": "bad_reference_table",
        "schema_type": "synapse",
        "segmentation_source": None,
        "table_metadata": {"reference_table": "anno_table"},
        "with_crud_columns": True,
    }

    ref_anno_model = make_model_from_schema(**table_args)
    assert not hasattr(ref_anno_model, "target_id")


def test_model_failure():
    class NestSchema(mm.Schema):
        a = mm.fields.Email()

    class BadSchema(mm.Schema):
        nest = mm.fields.Nested(NestSchema, many=True)

    with pytest.raises(UnknownAnnotationTypeException):
        make_model_from_schema("testBad", BadSchema)
    with pytest.raises(UnknownAnnotationTypeException):
        make_model_from_schema("testNest", NestSchema)
