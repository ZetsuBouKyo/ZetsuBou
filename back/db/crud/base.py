from datetime import datetime
from typing import AsyncIterator, Dict, List, Optional, Set, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import Column, delete, desc, text, update
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.sql import functions as func
from sqlalchemy.sql.elements import TextClause

from back.db.table import Base
from back.session.async_db import async_session

PydanticBaseModel = TypeVar("PydanticBaseModel", bound=BaseModel)


async def create(instance: DeclarativeMeta, data: Union[BaseModel, dict]) -> dict:
    if isinstance(data, BaseModel):
        data = data.model_dump()
    async with async_session() as session:
        data = instance(**data)
        async with session.begin():
            session.add(data)
        await session.refresh(data)
        return data.__dict__


async def batch_create(
    instance: DeclarativeMeta, data: Union[List[BaseModel], List[dict]]
):
    out = []
    async with async_session() as session:
        async with session.begin():
            for d in data:
                if isinstance(d, BaseModel):
                    d = d.model_dump()
                inst = instance(**d)
                session.add(inst)
                await session.flush()
                out.append(inst.__dict__)
    return out


async def count(instance: DeclarativeMeta, condition=None) -> int:
    async with async_session() as session:
        async with session.begin():
            statement = select(func.count()).select_from(instance)
            if condition is not None:
                statement = select(func.count()).select_from(instance).where(condition)
            rows = await session.execute(statement)
    return next(rows)[0]


async def count_total(instance: DeclarativeMeta) -> int:
    return await count(instance)


async def get_row_by(
    instance: DeclarativeMeta, condition, model: Type[PydanticBaseModel]
) -> Optional[PydanticBaseModel]:
    async with async_session() as session:
        async with session.begin():
            rows = await session.execute(select(instance).where(condition))
    first = rows.scalars().first()
    if first is None:
        return None
    return model(**first.__dict__)


async def get_row_by_id(
    instance: DeclarativeMeta, id, model: Type[PydanticBaseModel]
) -> Optional[PydanticBaseModel]:
    return await get_row_by(instance, instance.id == id, model)


async def get_rows_order_by(
    instance: DeclarativeMeta,
    order,
    model: Optional[Type[PydanticBaseModel]] = None,
    skip: int = 0,
    limit: int = 100,
    is_desc: bool = False,
) -> List[PydanticBaseModel]:
    out = []
    if is_desc:
        order = desc(order)
    async with async_session() as session:
        async with session.begin():
            rows = await session.execute(
                select(instance).offset(skip).limit(limit).order_by(order)
            )
        for row in rows.scalars().all():
            if model is None:
                row = row.__dict__
                del row["_sa_instance_state"]
                for k, v in row.items():
                    if isinstance(v, datetime):
                        row[k] = v.isoformat()
                out.append(row)
            else:
                out.append(model(**row.__dict__))
    return out


async def get_rows_order_by_id(
    instance: DeclarativeMeta,
    model: Type[PydanticBaseModel],
    skip: int = 0,
    limit: int = 100,
    is_desc: bool = False,
) -> List[PydanticBaseModel]:
    return await get_rows_order_by(
        instance, instance.id, model=model, skip=skip, limit=limit, is_desc=is_desc
    )


async def get_rows_by_condition_order_by(
    instance: DeclarativeMeta,
    condition,
    order,
    model: Type[PydanticBaseModel],
    skip: int = 0,
    limit: int = 100,
    is_desc: bool = False,
) -> List[PydanticBaseModel]:
    out = []
    if is_desc:
        order = desc(order)
    async with async_session() as session:
        async with session.begin():
            rows = await session.execute(
                select(instance)
                .where(condition)
                .offset(skip)
                .limit(limit)
                .order_by(order)
            )
        for row in rows.scalars().all():
            out.append(model(**row.__dict__))
    return out


async def get_rows_by_condition_order_by_id(
    instance: DeclarativeMeta,
    condition,
    model: Type[PydanticBaseModel],
    skip: int = 0,
    limit: int = 100,
    is_desc: bool = False,
) -> List[PydanticBaseModel]:
    return await get_rows_by_condition_order_by(
        instance, condition, instance.id, model, skip=skip, limit=limit, is_desc=is_desc
    )


async def get_rows_by_ids_order_by_id(
    instance: DeclarativeMeta,
    ids,
    model: Type[PydanticBaseModel],
    skip: int = 0,
    limit: int = 100,
    is_desc: bool = False,
) -> List[PydanticBaseModel]:
    return await get_rows_by_condition_order_by_id(
        instance, instance.id.in_(ids), model, skip=skip, limit=limit, is_desc=is_desc
    )


async def iter_by_condition_order_by_id(
    instance: DeclarativeMeta,
    condition,
    model: Type[PydanticBaseModel],
    limit: int = 100,
    is_desc: bool = False,
) -> AsyncIterator[PydanticBaseModel]:
    skip = 0
    rows = await get_rows_by_condition_order_by_id(
        instance, condition, model, skip=skip, limit=limit, is_desc=is_desc
    )
    while rows:
        for row in rows:
            yield row
        skip += limit
        rows = await get_rows_by_condition_order_by_id(
            instance, condition, model, skip=skip, limit=limit, is_desc=is_desc
        )


async def iter_order_by_id(
    instance: DeclarativeMeta,
    model: Type[PydanticBaseModel],
    limit: int = 100,
    is_desc: bool = False,
) -> AsyncIterator[PydanticBaseModel]:
    skip = 0
    rows = await get_rows_order_by_id(
        instance, model, skip=skip, limit=limit, is_desc=is_desc
    )
    while rows:
        for row in rows:
            yield row
        skip += limit
        rows = await get_rows_order_by_id(
            instance, model, skip=skip, limit=limit, is_desc=is_desc
        )


async def get_all_rows_by_condition_order_by(
    instance: DeclarativeMeta,
    condition,
    order,
    model: Type[PydanticBaseModel],
) -> List[PydanticBaseModel]:
    out = []
    skip = 0
    limit = 1000
    rows = await get_rows_by_condition_order_by(
        instance, condition, order, model, skip=skip, limit=limit
    )
    while rows:
        out += rows
        skip += limit
        rows = await get_rows_by_condition_order_by(
            instance, condition, order, model, skip=skip, limit=limit
        )

    return out


async def get_all_rows_by_condition_order_by_id(
    instance: DeclarativeMeta,
    condition,
    model: Type[PydanticBaseModel],
) -> List[PydanticBaseModel]:
    return await get_all_rows_by_condition_order_by(
        instance, condition, instance.id, model
    )


async def get_all_rows_order_by_id(instance: DeclarativeMeta) -> List[dict]:
    out = []
    skip = 0
    limit = 1000
    rows = await get_rows_order_by(instance, instance.id, skip=skip, limit=limit)
    while rows:
        out += rows
        skip += limit
        rows = await get_rows_order_by(instance, instance.id, skip=skip, limit=limit)

    return out


async def update_by(
    instance: DeclarativeMeta, condition, data: Union[Type[PydanticBaseModel], dict]
) -> bool:
    if isinstance(data, BaseModel):
        data = data.model_dump()

    async with async_session() as session:
        rows = await session.execute(update(instance).where(condition).values(**data))
        await session.commit()
        if rows.rowcount > 0:
            return True
        return False


async def update_by_id(
    instance: DeclarativeMeta, data: Union[Type[PydanticBaseModel], dict]
) -> bool:
    if isinstance(data, BaseModel):
        data = data.model_dump()
    return await update_by(instance, instance.id == data["id"], data)


async def overwrite_relation_between_tables(
    session: Session,
    data: BaseModel,
    data_parent_key: str,
    data_children_key: str,
    data_child_key: str,
    instance: DeclarativeMeta,
    instance_parent_col: Column,
    data_model: BaseModel,
) -> bool:
    new_children_ids = set(getattr(data, data_children_key))
    to_deleted_ids = set()

    rows = await session.execute(select(instance).where(instance_parent_col == data.id))
    for row in rows.scalars().all():
        d = data_model(**row.__dict__)
        child_id = getattr(d, data_child_key)
        if child_id not in new_children_ids:
            to_deleted_ids.add(d.id)
        else:
            new_children_ids.remove(child_id)

    while new_children_ids and to_deleted_ids:
        new_child_id = new_children_ids.pop()
        to_update_id = to_deleted_ids.pop()
        await session.execute(
            update(instance)
            .where(instance.id == to_update_id)
            .values(**{data_parent_key: data.id, data_child_key: new_child_id})
        )

    if new_children_ids:
        for child_id in new_children_ids:
            session.add(
                instance(**{data_parent_key: data.id, data_child_key: child_id})
            )
    if to_deleted_ids:
        for id in to_deleted_ids:
            await session.execute(delete(instance).where(instance.id == id))
    return True


async def delete_by(instance: DeclarativeMeta, condition) -> bool:
    rows = None
    async with async_session() as session:
        rows = await session.execute(delete(instance).where(condition))
        await session.commit()
    if rows is None:
        return False
    if rows.rowcount > 0:
        return True
    return False


async def delete_by_id(instance: DeclarativeMeta, id) -> bool:
    return await delete_by(instance, instance.id == id)


async def delete_all(instance: DeclarativeMeta):
    async with async_session() as session:
        await session.execute(delete(instance))
        await session.commit()


async def execute(
    statement: TextClause, async_engine: AsyncEngine = async_session.async_engine
) -> CursorResult:
    out = None
    async with async_engine.begin() as conn:
        out = await conn.execute(statement)
        await conn.commit()
    return out


def get_primary_key_names_by_table_instance(instance: DeclarativeMeta) -> List[str]:
    cols = instance.__mapper__.columns
    return [col.description for col in cols if col.primary_key]


def get_table_instances() -> Dict[str, Base]:
    table_instances = {}
    for mapper in Base.registry.mappers:
        if mapper.class_.__name__.endswith("Base"):
            table_instances[mapper.class_.__tablename__] = mapper.class_

    return table_instances


def get_dependent_tables(instance: DeclarativeMeta) -> Set[str]:
    table_names = set()
    attrs = [a for a in dir(instance) if not a.startswith("_")]
    for attr in attrs:
        attr = getattr(instance, attr)
        if type(attr) is InstrumentedAttribute:
            foreign_keys = attr.expression.foreign_keys
            for foreign_key in foreign_keys:
                colspec = foreign_key._get_colspec()
                table_name = colspec.split(".")[0]
                table_names.add(table_name)
    return table_names


def flatten_dependent_tables() -> List[str]:
    table_instances = get_table_instances()
    table_dependents = {
        table_name: get_dependent_tables(table_instance)
        for table_name, table_instance in table_instances.items()
    }

    visited = set()
    tables = []
    stack = [
        (table_name, dependents) for table_name, dependents in table_dependents.items()
    ]

    while stack:
        table_name, dependents = stack.pop(0)

        if table_name in visited:
            continue
        if dependents <= visited:
            visited.add(table_name)
            tables.append(table_name)
        else:
            stack.append((table_name, dependents))
    return tables


def table_exists(table_name: str):
    table_names = list_tables()
    if table_name not in table_names:
        raise ValueError(f"table: {table_name} did not exist")


def list_tables(base: DeclarativeMeta = Base) -> List[str]:
    _table_names = base.metadata.tables.keys()
    tables = list(_table_names)
    return tables


async def reset_auto_increment(
    table_name: str,
    seq: str = None,
    async_engine: AsyncEngine = async_session.async_engine,
) -> Optional[CursorResult]:
    try:
        table_exists(table_name)
    except ValueError:
        return

    if seq is None:
        seq = f"{table_name}_id_seq"
    statement = text(f'SELECT setval(:seq, MAX(id)) FROM "{table_name}";').bindparams(
        seq=seq
    )
    return await execute(statement, async_engine=async_engine)


async def get_seqs(async_engine: AsyncEngine = async_session.async_engine) -> List[str]:
    statement = text("SELECT * FROM information_schema.sequences;")
    rows = await execute(statement, async_engine=async_engine)
    return [row[2] for row in rows]
