from back.session.storage import get_app_storage_session


async def init_storage():
    session = get_app_storage_session(is_from_setting_if_none=True)
    async with session:
        await session.init()
