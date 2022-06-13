import logging
import os

from alembic import script
from alembic.command import upgrade
from alembic.config import Config
from alembic.runtime import migration
from sqlalchemy import create_engine


def run_migration(sql_url: str):
    migrations_dir = os.path.dirname(os.path.realpath(__file__))

    config_file = os.path.join(migrations_dir, "alembic.ini")

    config = Config(file_=config_file)
    config.set_main_option("script_location", migrations_dir)
    config.set_main_option("sqlalchemy.url", sql_url)

    engine = create_engine(sql_url)
    script_ = script.ScriptDirectory.from_config(config)
    with engine.begin() as conn:
        context = migration.MigrationContext.configure(conn)
        if context.get_current_revision() != script_.get_current_head():
            upgrade(config, "head")
        else:
            logging.info(f"Schema database up to date {script_.get_current_head()}")
    return True
