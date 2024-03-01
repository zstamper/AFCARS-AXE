from peewee import IntegerField, DateField

from playhouse.migrate import migrate

from model import ContextTable, SecondParent


def migration_0(migrator) -> None:
    """Inject the initial database version indicator as a bootstrap for future migrations."""
    from model import Version, database
    database.create_tables([Version])
    Version.get_or_create(database_version=0)


def migration_1(migrator) -> None:
    # Add support for the child's birth date in the child listing
    e5_field = DateField(null=True, formats=['%Y%m%d', '%m/%d/%Y', '%Y-%m-%d'])
    migrate(
        migrator.add_column('basechildtable', 'e5', e5_field)
    )


def migration_2(migrator) -> None:
    from model import ContextTable
    for context in ContextTable.select():
        if context.data and context.data.ooh and context.data.ooh.second_parents:
            number = 2
            for parent in context.data.ooh.second_parents:
                parent.number = number
                number += 1
        context.save()


def migration_3(migrator) -> None:
    from model import ContextTable
    for context in ContextTable.select():
        if hasattr(context.data, 'ooh') and hasattr(context.data.ooh, 'second_parents'):
            if len(context.data.ooh.second_parents) == 0:
                context.data.ooh.second_parents = [SecondParent(number=2)]
            else:
                i = 2
                for p in context.data.ooh.second_parents:
                    p.number = i
                    i += 1
            context.save()

