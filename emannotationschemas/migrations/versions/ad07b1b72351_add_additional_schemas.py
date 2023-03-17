"""Add additional schemas

Revision ID: ad07b1b72351
Revises: 34476f534ca9
Create Date: 2023-03-17 09:28:53.584860

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = "ad07b1b72351"
down_revision = "34476f534ca9"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "braincircuits_annotation_user",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("deleted", sa.DateTime(), nullable=True),
        sa.Column("superceded_id", sa.BigInteger(), nullable=True),
        sa.Column("valid", sa.Boolean(), nullable=True),
        sa.Column(
            "pt_position",
            Geometry(
                geometry_type="POINTZ",
                dimension=3,
                use_N_D_index=True,
                from_text="ST_GeomFromEWKT",
                name="geometry",
            ),
            nullable=True,
        ),
        sa.Column("tag", sa.String(), nullable=True),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_braincircuits_annotation_user_created"),
        "braincircuits_annotation_user",
        ["created"],
        unique=False,
    )
    op.create_index(
        op.f("ix_braincircuits_annotation_user_deleted"),
        "braincircuits_annotation_user",
        ["deleted"],
        unique=False,
    )
    op.create_table(
        "representative_point",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("deleted", sa.DateTime(), nullable=True),
        sa.Column("superceded_id", sa.BigInteger(), nullable=True),
        sa.Column("valid", sa.Boolean(), nullable=True),
        sa.Column(
            "pt_position",
            Geometry(
                geometry_type="POINTZ",
                dimension=3,
                use_N_D_index=True,
                from_text="ST_GeomFromEWKT",
                name="geometry",
            ),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_representative_point_created"),
        "representative_point",
        ["created"],
        unique=False,
    )
    op.create_index(
        op.f("ix_representative_point_deleted"),
        "representative_point",
        ["deleted"],
        unique=False,
    )
    op.create_table(
        "braincircuits_annotation_user__tests_pcg",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("pt_supervoxel_id", sa.BigInteger(), nullable=True),
        sa.Column("pt_root_id", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id"],
            ["braincircuits_annotation_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_braincircuits_annotation_user__tests_pcg_pt_root_id"),
        "braincircuits_annotation_user__tests_pcg",
        ["pt_root_id"],
        unique=False,
    )
    op.create_table(
        "func_unit_ext_coreg",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("deleted", sa.DateTime(), nullable=True),
        sa.Column("superceded_id", sa.BigInteger(), nullable=True),
        sa.Column("valid", sa.Boolean(), nullable=True),
        sa.Column("target_id", sa.BigInteger(), nullable=True),
        sa.Column("session", sa.Integer(), nullable=True),
        sa.Column("scan_idx", sa.Integer(), nullable=True),
        sa.Column("unit_id", sa.Integer(), nullable=True),
        sa.Column("field", sa.Integer(), nullable=True),
        sa.Column("residual", sa.Float(), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["target_id"],
            ["reference_table.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_func_unit_ext_coreg_created"),
        "func_unit_ext_coreg",
        ["created"],
        unique=False,
    )
    op.create_index(
        op.f("ix_func_unit_ext_coreg_deleted"),
        "func_unit_ext_coreg",
        ["deleted"],
        unique=False,
    )
    op.create_index(
        op.f("ix_func_unit_ext_coreg_target_id"),
        "func_unit_ext_coreg",
        ["target_id"],
        unique=False,
    )
    op.create_table(
        "representative_point__tests_pcg",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("pt_supervoxel_id", sa.BigInteger(), nullable=True),
        sa.Column("pt_root_id", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id"],
            ["representative_point.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_representative_point__tests_pcg_pt_root_id"),
        "representative_point__tests_pcg",
        ["pt_root_id"],
        unique=False,
    )
    op.create_table(
        "simple_reference",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("deleted", sa.DateTime(), nullable=True),
        sa.Column("superceded_id", sa.BigInteger(), nullable=True),
        sa.Column("valid", sa.Boolean(), nullable=True),
        sa.Column("target_id", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["target_id"],
            ["reference_table.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_simple_reference_created"),
        "simple_reference",
        ["created"],
        unique=False,
    )
    op.create_index(
        op.f("ix_simple_reference_deleted"),
        "simple_reference",
        ["deleted"],
        unique=False,
    )
    op.create_index(
        op.f("ix_simple_reference_target_id"),
        "simple_reference",
        ["target_id"],
        unique=False,
    )
    op.create_table(
        "func_unit_ext_coreg__tests_pcg",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["func_unit_ext_coreg.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "simple_reference__tests_pcg",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["simple_reference.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("simple_reference__tests_pcg")
    op.drop_table("func_unit_ext_coreg__tests_pcg")
    op.drop_index(op.f("ix_simple_reference_target_id"), table_name="simple_reference")
    op.drop_index(op.f("ix_simple_reference_deleted"), table_name="simple_reference")
    op.drop_index(op.f("ix_simple_reference_created"), table_name="simple_reference")
    op.drop_table("simple_reference")
    op.drop_index(
        op.f("ix_representative_point__tests_pcg_pt_root_id"),
        table_name="representative_point__tests_pcg",
    )
    op.drop_table("representative_point__tests_pcg")
    op.drop_index(
        op.f("ix_func_unit_ext_coreg_target_id"), table_name="func_unit_ext_coreg"
    )
    op.drop_index(
        op.f("ix_func_unit_ext_coreg_deleted"), table_name="func_unit_ext_coreg"
    )
    op.drop_index(
        op.f("ix_func_unit_ext_coreg_created"), table_name="func_unit_ext_coreg"
    )
    op.drop_table("func_unit_ext_coreg")
    op.drop_index(
        op.f("ix_braincircuits_annotation_user__tests_pcg_pt_root_id"),
        table_name="braincircuits_annotation_user__tests_pcg",
    )
    op.drop_table("braincircuits_annotation_user__tests_pcg")
    op.drop_index(
        op.f("ix_representative_point_deleted"), table_name="representative_point"
    )
    op.drop_index(
        op.f("ix_representative_point_created"), table_name="representative_point"
    )
    op.drop_table("representative_point")
    op.drop_index(
        op.f("ix_braincircuits_annotation_user_deleted"),
        table_name="braincircuits_annotation_user",
    )
    op.drop_index(
        op.f("ix_braincircuits_annotation_user_created"),
        table_name="braincircuits_annotation_user",
    )
    op.drop_table("braincircuits_annotation_user")
