import marshmallow as mm
from emannotationschemas.schemas.base import (
    AnnotationSchema,
    BoundSpatialPoint,
    NumericField,
    ReferenceAnnotation,
)


class CellMatch(AnnotationSchema):
    """Schema for matching cells between datasets"""

    pt = mm.fields.Nested(
        BoundSpatialPoint,
        required=True,
        description="Source cell identity (pt_root_id, pt_supervoxel_id, pt_position)",
    )
    query_root_id = NumericField(
        required=True,
        description="Static root ID used for score calculation",
    )
    match_id = mm.fields.Str(
        required=True,
        description="Unique identifier for cell from another dataset",
        index=True,
    )
    score = mm.fields.Float(
        required=True,
        description="Normalised NBLAST similarity score [for CAVE schema, could be any numeric score]",
    )
    validation = mm.fields.Bool(
        required=False,
        default=False,
        description="False if not separately validated, True if separately validated",
    )


class CellSimilarity(AnnotationSchema):
    """Schema for cell similarity scoring between two cells"""

    pt = mm.fields.Nested(
        BoundSpatialPoint,
        required=True,
        description="Query cell identity (pt_root_id, pt_supervoxel_id, pt_position)",
    )
    match_pt = mm.fields.Nested(
        BoundSpatialPoint,
        required=True,
        description="Target cell identity (match_root_id, match_supervoxel_id, match_position)",
    )
    query_root_id = NumericField(
        required=True,
        description="Static root ID for query cell at time of score calculation",
    )
    match_root_id = NumericField(
        required=True,
        description="Static root ID for target cell at time of score calculation",
    )
    score = mm.fields.Float(
        required=True,
        description="Numeric similarity score between the two cells",
    )


class CellMatchReference(ReferenceAnnotation):
    """Reference annotation version of CellMatch schema"""

    query_root_id = NumericField(
        required=True,
        description="Static root ID used for score calculation",
    )
    match_id = mm.fields.Str(
        required=True,
        description="Unique identifier for cell from another dataset",
        index=True,
    )
    score = mm.fields.Float(
        required=True,
        description="Normalized NBLAST similarity score [for CAVE schema, could be any numeric score]",
    )
    validation = mm.fields.Bool(
        required=False,
        default=False,
        description="False if not validated by a human, True if validated by a human",
    )
