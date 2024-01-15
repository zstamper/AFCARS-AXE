from peewee import IntegerField

from playhouse.migrate import migrate

from model import Version, database


def migration_0(migrator) -> None:
    """Inject the initial database version indicator as a bootstrap for future migrations."""
    database.create_tables([Version])
    database_version_field = IntegerField(default=0)

    migrate(
        migrator.add_column('version', 'database_version', database_version_field)
    )
