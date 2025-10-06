from logging.config import fileConfig
from sqlmodel import SQLModel
from sqlalchemy import create_engine, pool
from app.config.env import EnvConfig
from alembic import context

# Load environment configuration
env_config = EnvConfig() # type: ignore

# Alembic configuration object
config = context.config

# Ensure the URL is converted to a synchronous dialect for Alembic
SYNC_DATABASE_URL = env_config.DATABASE_URI.replace("postgresql+asyncpg", "postgresql")

config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)

# Set up logging if a config file exists
if config.config_file_name:
    fileConfig(config.config_file_name)

# Metadata for 'autogenerate'
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (without a database connection)."""
    context.configure(
        url=SYNC_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (with a database connection)."""
    connectable = create_engine(SYNC_DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()