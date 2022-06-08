import os

from alembic.command import upgrade
from alembic.config import Config


def run_migration(sql_url: str):
    migrations_dir = os.path.dirname(os.path.realpath(__file__))

    config_file = os.path.join(migrations_dir, "alembic.ini")

    config = Config(file_=config_file)
    config.set_main_option("script_location", migrations_dir)
    config.set_main_option("sqlalchemy.url", sql_url)
    upgrade(config, "head")
