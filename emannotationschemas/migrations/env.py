from logging.config import fileConfig

from alembic import context
from emannotationschemas import type_mapping
from emannotationschemas.models import Base, make_dataset_models
from emannotationschemas.schemas.base import ReferenceTableField
from geoalchemy2.alembic_helpers import include_object, render_item
from sqlalchemy import BigInteger, Column, engine_from_config, pool

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def parse_schemas():
    metadata_dict = {}
    for schema_name, schema_type in type_mapping.items():
        Schema = schema_type()
        for field_name, field_type in Schema.declared_fields.items():
            if isinstance(field_type, ReferenceTableField):
                metadata_dict[schema_name] = {"reference_table": "reference_table"}
    return metadata_dict


def make_models():
    model_names = [(schema_name, f"{schema_name}") for schema_name in type_mapping]
    metadata_dict = parse_schemas()
    model_dict = make_dataset_models("test", model_names, metadata_dict=metadata_dict)
    model_dict = make_dataset_models(
        "test",
        model_names,
        segmentation_source="tests_pcg",
        metadata_dict=metadata_dict,
        with_crud_columns=False,
    )
    return Base


models = make_models()

target_metadata = models.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_item=render_item,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
            include_object=include_object,
        )
        target_metadata.bind = connectable
        target_metadata.reflect()

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
