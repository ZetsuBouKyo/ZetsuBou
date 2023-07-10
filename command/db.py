from typing import List

import typer
from rich import print_json
from rich.console import Console
from rich.table import Table
from sqlalchemy import text

from back.db.crud.base import (
    get_all_rows_order_by_id,
    get_dependent_tables,
    get_seqs,
    get_table_instances,
    list_tables,
    reset_auto_increment,
)
from back.session.async_db import async_engine, async_session
from lib.typer import ZetsuBouTyper

_help = """
Manipulate the SQL databases.
"""
app = ZetsuBouTyper(name="db", help=_help)


@app.command()
async def execute(sql: str = typer.Argument(..., help="SQL.")):
    async with async_engine.begin() as conn:
        statement = text(sql)
        rows = await conn.execute(statement)
        await conn.commit()
        for row in rows:
            print(row)


@app.command()
async def list_schemas():
    """
    List the schemas.
    """

    async with async_session() as session:
        statement = text("select * from information_schema.tables")
        rows = await session.execute(statement)

        table = Table(title="ZetsuBou's SQL database schemas")
        table.add_column("table_catalog")
        table.add_column("table_schema")
        table.add_column("table_name")
        table.add_column("table_type")
        table.add_column("self_referencing_column_name")
        table.add_column("reference_generation")
        table.add_column("user_defined_type_catalog")
        table.add_column("user_defined_type_schema")
        table.add_column("user_defined_type_name")
        table.add_column("is_insertable_into")
        table.add_column("is_typed")
        table.add_column("commit_action")

        for row in rows:
            _row = list(row.tuple())
            table.add_row(*_row)

    console = Console()
    console.print(table)


@app.command()
async def drop_table(table_name: str = typer.Argument(..., help="Table name.")):
    tables = list_tables()
    if table_name not in tables:
        return
    sql = f"DROP TABLE IF EXISTS {table_name}, permission CASCADE;"
    async with async_engine.begin() as conn:
        statement = text(sql)
        await conn.execute(statement)
        await conn.commit()


@app.command(name="list-tables")
def _list_tables(
    total: bool = typer.Option(
        default=False, help="Show the total number of tables in the last line."
    ),
    rich: bool = typer.Option(default=True, help="Show the tables in Rich mode."),
) -> List[str]:
    """
    List the SQL databases.
    """
    tables = list_tables()
    if rich:
        table = Table(title="ZetsuBou's SQL database tables")
        table.add_column("Name")
        for name in tables:
            table.add_row(name)
        if total:
            table.add_row("")
            table.add_row(f"\ntotal: {len(tables)}")
        console = Console()
        console.print(table)
        return
    for table in tables:
        print(table)
    if total:
        print(f"\ntotal: {len(tables)}")


@app.command()
def tree():
    """
    Show the depentencies between tables.
    """
    table_instances = get_table_instances()
    for table_name, table_instance in table_instances.items():
        table = Table()
        table.add_column("Parents")
        table.add_column("Child")
        parents = get_dependent_tables(table_instance)
        parents = list(parents)
        parents.sort()

        if len(parents) > 0:
            for i, parent in enumerate(parents):
                if i == 0:
                    table.add_row(parent, table_name)
                else:
                    table.add_row(parent, "")
        else:
            table.add_row("", table_name)

        console = Console()
        console.print(table)


@app.command(name="reset-auto-increment")
async def _reset_auto_increment(
    table_name: str = typer.Argument(..., help="Table name.")
):
    """
    Reset the auto increment in PostgreSQL.
    """
    await reset_auto_increment(table_name)


@app.command()
async def list_seqs():
    """
    List the sequences.
    """
    seqs = await get_seqs()
    if not seqs:
        return
    for seq in seqs:
        print(seq)


@app.command(name="list")
async def _list(table_name: str = typer.Argument(..., help="Table name.")):
    table_instances = get_table_instances()
    table_class = table_instances[table_name]
    rows = await get_all_rows_order_by_id(table_class)
    print_json(data=rows)
