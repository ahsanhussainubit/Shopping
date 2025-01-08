from __future__ import with_statement
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base  # Import your Base here

# Configure the Alembic logging
fileConfig(context.config.config_file_name)

# This is the target metadata that Alembic will use to compare the models
target_metadata = Base.metadata

# Setup the configuration and the engine
def run_migrations_offline():
    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# Determine if we're running offline or online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
