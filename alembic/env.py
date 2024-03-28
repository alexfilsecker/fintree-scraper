from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from typing import Dict, Union

from src import models

import os

target_metadata = models.Base.metadata


def get_connection_uri():
    db_user = os.environ.get("POSTGRES_USER")
    db_password = os.environ.get("POSTGRES_PASSWORD")
    db_db = os.environ.get("POSTGRES_DB")
    db_host = os.environ.get("POSTGRES_HOST")
    if db_user is None or db_password is None or db_db is None or db_host is None:
        print("ASUMING INSIDE LOCAL MACHINE. NOT DOCKER CONTAINER")
        envs: Dict[str, Union[str, None]] = dict()
        with open(".envs/.env.postgres", "r") as f:
            lines = f.readlines()

        for line in lines:
            if line.strip() == "":
                continue
            envs[line.split("=")[0]] = line.split("=")[1].strip()

        db_user = envs.get("POSTGRES_USER")
        db_password = envs.get("POSTGRES_PASSWORD")
        db_db = envs.get("POSTGRES_DB")
        db_host = "localhost"

    return f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_db}"


config = context.config
config.set_main_option("sqlalchemy.url", get_connection_uri())

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
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
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
