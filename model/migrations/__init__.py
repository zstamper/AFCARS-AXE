from peewee import IntegerField, DateField

from playhouse.migrate import migrate

from model import Version, database


def migration_0(migrator) -> None:
    """Inject the initial database version indicator as a bootstrap for future migrations."""
    database.create_tables([Version])
    Version.get_or_create(database_version=0)


def migration_1(migrator) -> None:
    # Add support for the child's birth date in the child listing
    e5_field = DateField(null=True, formats=['%Y%m%d', '%m/%d/%Y', '%Y-%m-%d'])
    migrate(
        migrator.add_column('basechildtable', 'e5', e5_field)
    )
