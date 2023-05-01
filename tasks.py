# import asyncio
# import json
# import os

# import aioredis
# from celery import Celery

# from back.crud.gallery import CrudSyncGallery

# unique_tasks = {
#     "sync_gallery": "sync_gallery",
#     "sync_all_galleries": "sync_gallery",
#     "sync_images": "sync_images",
#     "sync_images_zetsubou_all": "sync_images",
#     "sync_images_zetsubou_group": "sync_images",
# }

# loop = asyncio.get_event_loop()

# try:
#     redis_url = os.environ["REDIS_URL"]
# except KeyError:
#     redis_url = "redis://localhost:6379"

# redis = aioredis.from_url(redis_url)

# celery_app = Celery(
#     "tasks",
#     backend=redis_url,
#     broker=redis_url,
#     result_extended=True,
#     task_track_started=True,
# )


# async def is_running(task_name: str) -> bool:
#     group_task_name = unique_tasks.get(task_name, None)
#     if group_task_name is None:
#         return False

#     async for key in redis.scan_iter(match="celery-task-meta*"):
#         t = await redis.type(key)

#         value = None
#         if t != b"string":
#             continue

#         value = await redis.get(key)
#         value.decode("utf-8")
#         value = json.loads(value)

#         tmp_task_name = value.get("name", None)
#         if tmp_task_name is None:
#             continue

#         tmp_group_task_name = unique_tasks.get(task_name, None)
#         if tmp_group_task_name is None:
#             continue

#         tmp_status = value.get("status", None)
#         if tmp_status != "SUCCESS":
#             return True

#     return False


# # def is_running(task_name: str):
# #     all_tasks = celery_app.control.inspect().active()
# #     for tasks in all_tasks.values():
# #         for task in tasks:
# #             existed_task_name = task.get("name", None)
# #             if existed_task_name is None:
# #                 continue
# #             if unique_tasks[task_name] == unique_tasks[existed_task_name]:
# #                 return True
# #     return False


# @celery_app.task(name="sync_all_galleries")
# def sync_all_galleries():
#     crud = CrudSyncGallery()
#     asyncio.run(crud.sync_all_galleries())
#     # TODO: log
#     print("finished")
#     return True


# # @celery_app.task(name="sync_gallery_new")
# # def sync_gallery_new():
# #     print(sync_gallery_new.name)
# #     crud = Crudgalleryync()
# #     crud.sync_new()
# #     # TODO: log
# #     print("finished")
# #     return True


# # @celery_app.task(name="sync_images_zetsubou_all")
# # def sync_images_zetsubou_all():
# #     crud = CrudImageSync()
# #     crud.sync_zetsubou_all()
# #     # TODO: log
# #     print("finished")
# #     return True


# # @celery_app.task(name="sync_images_zetsubou_group")
# # def sync_images_zetsubou_group(group_name: str, group_path: str):
# #     crud = CrudImageSync()
# #     crud.sync_zetsubou_group(group_name, group_path)
# #     # TODO: log
# #     print("finished")
# #     return True
