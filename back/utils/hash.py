from hashlib import md5
from pathlib import Path


def get_md5(fpath: Path):
    hash_md5 = md5()
    with fpath.open(mode="rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
