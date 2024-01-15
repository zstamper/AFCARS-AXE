from peewee import IntegerField

from playhouse.migrate import migrate

from model import Version, database


def migration_0(migrator) -> None:
    """Inject the initial database version indicator as a bootstrap for future migrations."""
    database.create_tables([Version])
    Version.get_or_create(database_version=0)
