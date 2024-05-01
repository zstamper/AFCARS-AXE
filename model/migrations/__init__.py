# Copyright 2024 by ICF International, Inc.
#
# This file is part of AXE, the AFCARS XML Editor.
#
# AXE is free software: you can redistribute it and/or modify it under the terms
# of the GNU Lesser General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# AXE is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# AXE. If not, see <https://www.gnu.org/licenses/>.

from peewee import DateField
from playhouse.migrate import migrate

from model import SecondParent


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
