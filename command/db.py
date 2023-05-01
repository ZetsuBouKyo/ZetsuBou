from typing import List

from back.db.crud.base import (
    get_dependent_tables,
    get_seqs,
    get_table_instances,
    list_tables,
    reset_auto_increment,
)
from back.session.async_db import async_engine, async_session
from sqlalchemy import text

from command.utils import sync


class Db:
    """Operations for RDBMS in ZetsuBou."""

    @sync
    async def list_schema(self):
        async with async_session() as session:
            rows = await session.execute("select * from information_schema.tables")
            for row in rows:
                print(row)

    # TODO: deprecated
    @sync
    async def drop_permission_tables(self):
        async with async_engine.begin() as conn:
            statement = text(
                "DROP TABLE IF EXISTS group_permission, permission CASCADE;"
            )
            await conn.execute(statement)
            await conn.commit()

    def list(self, total: bool = False) -> List[str]:
        tables = list_tables()
        for table in tables:
            print(table)
        if total:
            print(f"\ntotal: {len(tables)}")
        return tables

    def tree(self):
        table_instances = get_table_instances()
        for table_name, table_instance in table_instances.items():
            print(f"table: {table_name}")
            print(get_dependent_tables(table_instance))

    @sync
    async def reset_auto_increment(self, table_name: str):
        await reset_auto_increment(table_name)

    @sync
    async def list_seqs(self):
        seqs = await get_seqs()
        if not seqs:
            return
        for seq in seqs:
            print(seq)
