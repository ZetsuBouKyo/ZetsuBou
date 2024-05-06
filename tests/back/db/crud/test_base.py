import pytest
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from back.db.crud.base import (
    batch_create,
    count,
    count_total,
    create,
    delete_all,
    delete_by,
    delete_by_id,
    flatten_dependent_tables,
    get_all_rows_by_condition_order_by,
    get_all_rows_by_condition_order_by_id,
    get_all_rows_order_by_id,
    get_dependent_tables,
    get_primary_key_names_by_table_instance,
    get_row_by,
    get_row_by_id,
    get_rows_by_condition_order_by,
    get_rows_by_condition_order_by_id,
    get_rows_by_ids_order_by_id,
    get_rows_order_by,
    get_rows_order_by_id,
    get_table_instances,
    iter_by_condition_order_by_id,
    iter_order_by_id,
    list_tables,
    reset_auto_increment,
    table_exists,
    update_by,
    update_by_id,
)
from lib.faker import ZetsuBouFaker
from tests.general.logging import logger
from tests.general.session import DatabaseSession

Base = declarative_base()
table_name = "tests_a"


class A(Base):
    __tablename__: str = table_name
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))


class AModelCreate(BaseModel):
    name: str


class AModelCreated(AModelCreate):
    id: int


AModel = AModelUpdate = AModelCreated


class TableSession(DatabaseSession):
    def __init__(self, row_num: int = 0):
        self.row_num = row_num

    async def create_table(self):
        async with self.async_session.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create_data(self):
        faker = ZetsuBouFaker()
        for _ in range(self.row_num):
            row = {"name": faker.name()}
            await create(A, row)

    async def enter(self):
        await self.create_table()
        await self.create_data()

    async def exit(self):
        async with self.async_session.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_table_session():
    async with TableSession():
        ...
    tables = list_tables()
    assert len(tables) > 0


@pytest.mark.asyncio
@pytest.mark.integration
async def test_batch_create():
    async with TableSession():
        faker = ZetsuBouFaker()
        num = 5
        rows_1 = [{"name": faker.name()} for _ in range(num)]
        await batch_create(A, rows_1)

        c_1 = await count_total(A)
        assert c_1 == num

        rows_2 = [AModelCreate(name=faker.name()) for _ in range(num)]
        await batch_create(A, rows_2)

        c_2 = await count_total(A)
        assert c_2 == num + num


@pytest.mark.asyncio
@pytest.mark.integration
async def test_crud():
    async with TableSession():
        faker = ZetsuBouFaker()
        row_1 = {"name": faker.name()}
        row_1_created = await create(A, row_1)
        row_1_created = AModel(**row_1_created)
        logger.info(f"ID: {row_1_created.id}")
        logger.info(f"name: {row_1_created.name}")

        row_2 = AModelCreate(name=faker.name())
        row_2_created = await create(A, row_2)
        row_2_created = AModel(**row_2_created)
        logger.info(f"ID: {row_2_created.id}")
        logger.info(f"name: {row_2_created.name}")

        c_1 = await count(A, A.id == row_1_created.id)
        assert c_1 == 1

        c_2 = await count(A)
        assert c_2 == 2

        c_3 = await count_total(A)
        assert c_3 == 2

        row_1_get_row_by = await get_row_by(A, A.id == row_1_created.id, AModel)
        assert row_1_get_row_by is not None
        assert row_1_get_row_by.id == row_1_created.id
        assert row_1_get_row_by.name == row_1_created.name

        row_1_get_row_by_id = await get_row_by_id(A, row_1_created.id, AModel)
        assert row_1_get_row_by_id is not None
        assert row_1_get_row_by_id.id == row_1_created.id
        assert row_1_get_row_by_id.name == row_1_created.name

        row_name_1_to_update = faker.name()
        row_1_to_update = {"id": row_1_created.id, "name": row_name_1_to_update}
        await update_by(A, A.id == row_1_created.id, row_1_to_update)
        row_1_updated = await get_row_by_id(A, row_1_created.id, AModel)
        assert row_1_updated.id == row_1_created.id
        assert row_1_updated.name == row_name_1_to_update

        row_name_2_to_update = faker.name()
        row_2_to_update = AModelUpdate(id=row_2_created.id, name=row_name_2_to_update)
        await update_by(A, A.id == row_2_created.id, row_2_to_update)
        row_2_updated = await get_row_by_id(A, row_2_created.id, AModel)
        assert row_2_updated.id == row_2_created.id
        assert row_2_updated.name == row_name_2_to_update

        row_3 = AModelCreate(name=faker.name())
        row_3_created = await create(A, row_3)
        row_3_created = AModel(**row_3_created)
        logger.info(f"ID: {row_3_created.id}")
        logger.info(f"name: {row_3_created.name}")

        row_name_3_to_update_1 = faker.name()
        row_3_to_update_1 = AModelUpdate(
            id=row_3_created.id, name=row_name_3_to_update_1
        )
        await update_by_id(A, row_3_to_update_1)
        row_3_updated_1 = await get_row_by_id(A, row_3_created.id, AModel)
        assert row_3_updated_1.id == row_3_created.id
        assert row_3_updated_1.name == row_name_3_to_update_1

        row_name_3_to_update_2 = faker.name()
        row_3_to_update_2 = {"id": row_3_created.id, "name": row_name_3_to_update_2}
        await update_by_id(A, row_3_to_update_2)
        row_3_updated_2 = await get_row_by_id(A, row_3_created.id, AModel)
        assert row_3_updated_2.id == row_3_created.id
        assert row_3_updated_2.name == row_name_3_to_update_2

        await delete_by(A, A.id == row_1_created.id)
        row_1_deleted = await get_row_by_id(A, row_1_created.id, AModel)
        assert row_1_deleted is None

        await delete_by_id(A, row_2_created.id)
        row_2_deleted = await get_row_by_id(A, row_2_created.id, AModel)
        assert row_2_deleted is None

        await delete_all(A)
        row_3_deleted = await get_row_by_id(A, row_3_created.id, AModel)
        assert row_3_deleted is None


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_rows_and_iter():
    num = 20
    async with TableSession(row_num=num):
        c_0 = await count_total(A)
        assert c_0 == num

        # test `get_rows_*`
        limit_1 = 5
        rows_1 = await get_rows_order_by(A, A.id, limit=limit_1)
        assert len(rows_1) == limit_1
        i = 0
        for row in rows_1:
            id = row.get("id", None)
            assert id is not None
            assert id > i
            i = id

        limit_2 = 5
        rows_2 = await get_rows_order_by(
            A, A.id, model=AModel, limit=limit_2, is_desc=True
        )
        i = float("inf")
        for row in rows_2:
            id = row.id
            assert id is not None
            assert id < i
            i = id

        limit_3 = 5
        rows_3 = await get_rows_order_by_id(A, AModel, limit=limit_3)
        limit_4 = 5
        rows_4 = await get_rows_order_by_id(A, AModel, skip=limit_3, limit=limit_4)
        assert rows_3[0].id + 5 == rows_4[0].id

        row_id_4 = 1
        rows_4 = await get_rows_by_condition_order_by(A, A.id == row_id_4, A.id, AModel)
        assert rows_4[0].id == row_id_4

        row_ids_5 = [1, 3, 5]
        rows_5 = await get_rows_by_condition_order_by_id(A, A.id.in_(row_ids_5), AModel)
        for i in range(len(row_ids_5)):
            assert row_ids_5[i] == rows_5[i].id

        row_ids_6 = list(range(1, 10, 2))
        rows_6 = await get_rows_by_ids_order_by_id(A, row_ids_6, AModel)
        i = 0
        for j in range(len(row_ids_6)):
            assert row_ids_6[j] == rows_6[j].id
            assert i < rows_6[j].id
            i = rows_6[j].id

        row_ids_7 = list(range(1, 10, 2))
        rows_7 = await get_rows_by_ids_order_by_id(A, row_ids_7, AModel, is_desc=True)
        i = float("inf")
        for j in range(len(row_ids_7)):
            assert rows_7[j].id in row_ids_7
            assert i > rows_7[j].id
            i = rows_7[j].id

        # test `iter_*`
        i = float("inf")
        c = 0
        async for row in iter_order_by_id(A, AModel, is_desc=True, limit=5):
            assert i > row.id
            i = row.id
            c += 1
        assert c == num

        c = 0
        row_ids_8 = [1, 3, 5]
        async for row in iter_by_condition_order_by_id(A, A.id.in_(row_ids_8), AModel):
            assert row.id in row_ids_8
            c += 1
        assert c == len(row_ids_8)

        # test `get_all_rows_*`
        row_ids_9 = [1, 3, 5, 7, 9]
        rows_9 = await get_all_rows_by_condition_order_by(
            A, A.id.in_(row_ids_9), A.id, AModel
        )
        assert len(rows_9) == len(row_ids_9)
        i = 0
        for row in rows_9:
            assert i < row.id
            i = row.id

        row_ids_10 = [1, 3, 5, 7, 9]
        rows_10 = await get_all_rows_by_condition_order_by_id(
            A, A.id.in_(row_ids_10), AModel
        )
        assert len(rows_10) == len(row_ids_10)
        i = 0
        for row in rows_10:
            assert i < row.id
            i = row.id

        rows_11 = await get_all_rows_order_by_id(A)
        assert len(rows_11) == num


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_rows_none():
    async with TableSession():
        rows_1 = await get_rows_order_by(A, A.id)
        assert len(rows_1) == 0

        rows_2 = await get_rows_by_condition_order_by(A, A.id == 1, A.id, AModel)
        assert len(rows_2) == 0


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_rows():
    num = 100
    async with TableSession(row_num=num):
        rows = await get_all_rows_order_by_id(A)
        assert len(rows) == num


@pytest.mark.integration
def test_table():
    table_names_1 = list_tables()
    for table_name in table_names_1:
        table_exists(table_name)

    faker = ZetsuBouFaker()
    table_name = faker.random_string(20)
    with pytest.raises(ValueError):
        table_exists(table_name)

    table_names_2 = flatten_dependent_tables()
    assert len(table_names_2) == len(table_names_1)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_reset_auto_increment():
    table_instances = get_table_instances()
    for _, table_instance in table_instances.items():
        pk_names = get_primary_key_names_by_table_instance(table_instance)
        for pk_name in pk_names:
            seq = f"{table_name}_{pk_name}_seq"
            await reset_auto_increment(table_name, seq=seq)
