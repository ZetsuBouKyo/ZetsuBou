# TODO:
# import json
# from pathlib import Path
# from uuid import uuid4

# from back.crud.repo import CrudRepoEx
# from back.model.image import Image, Images
# from back.settings import setting
# from back.utils.dt import second2iso
# from back.utils.image import is_image
# from back.utils.hash import get_md5
# from cv2 import imread


# class CrudImageSync:
#     def __init__(self):
#         self.imgs_fname = setting.repo.imgs_fname
#         self.dir_fname = setting.repo.dir_fname

#     def sync_zetsubou_repo(self, group: str, repo_path: Path):
#         changed = False

#         repo = CrudRepoEx(group=group, path=repo_path)
#         repo = repo.tag

#         imgs = Images()
#         imgs_path = repo_path / self.dir_fname / self.imgs_fname
#         if imgs_path.exists():
#             with imgs_path.open(mode="r") as fp:
#                 imgs = json.load(fp)
#                 imgs = Images(**imgs)

#         for fname in imgs.data.keys():
#             fpath = repo_path / fname
#             if not fpath.exists():
#                 changed = True
#                 del imgs.data[fname]

#         for img_fpath in repo_path.iterdir():
#             if not is_image(img_fpath):
#                 continue

#             fname = img_fpath.name
#             mtime = second2iso(img_fpath.stat().st_mtime)

#             old_img = imgs.data.get(fname, None)
#             if old_img is not None and mtime == old_img.mtime:
#                 continue

#             changed = True

#             id = str(uuid4())
#             img_arr = imread(str(img_fpath))
#             width, height, _ = img_arr.shape
#             md5 = get_md5(img_fpath)

#             imgs.data[fname] = Image(
#                 **{
#                     "id": id,
#                     "repo_id": repo.id,
#                     "width": width,
#                     "height": height,
#                     "slope": height / width,
#                     "fname": fname,
#                     "md5": md5,
#                     "mtime": mtime,
#                 }
#             )
#         if changed:
#             with imgs_path.open(mode="w", encoding="utf-8") as fp:
#                 json.dump(imgs.dict(), fp, indent=4, ensure_ascii=False)

#     def sync_zetsubou_group(self, group_name: str, group_path: str):
#         group_path = Path(group_path)
#         for repo_path in group_path.iterdir():
#             self.sync_zetsubou_repo(group_name, repo_path)

#     def sync_zetsubou_all(self):
#         for group_name, group_path in setting.repo.group.items():
#             self.sync_zetsubou_group(group_name, group_path)
