import mimetypes
import os
import subprocess
from pathlib import Path

reserved_symbols = ["#"]


def remove_reserved_symbols(fpath: Path):
    if fpath.is_dir():
        print(f"path: {fpath} is dir")
        return
    new_name = fpath.name

    to_rename = False
    for symbol in reserved_symbols:
        if symbol in fpath.name:
            to_rename = True
            print(f"path: {fpath} needs to be renamed")
        new_name = new_name.replace(symbol, "")

    if not to_rename:
        return

    new_name.replace("   ", " ")
    new_name.replace("  ", " ")
    new_path = fpath.parent / new_name
    fpath.rename(new_path)


class Video:
    """Operations for Video in ZetsuBou."""

    def remove_reserved_symbols(self, home: str):
        home = Path(home)
        for fpath in home.glob("**/*"):
            if fpath.is_dir():
                for symbol in reserved_symbols:
                    if symbol in str(fpath):
                        print(fpath)
                continue
            remove_reserved_symbols(fpath)

    def remove_broken(self, home: str):
        home = Path(home)
        for fpath in home.glob("**/*"):
            if fpath.is_dir():
                continue

            if fpath.stat().st_size == 0:
                fpath.unlink()

    def to_h264(self, src: str, dest: str, limit: int = None):
        root = Path(src)
        root_h264 = Path(dest)

        c = 0
        for f in root.rglob("**/*"):
            f_h264 = root_h264 / f.relative_to(root).parent / f"{f.name}.h264.mp4"
            if f_h264.exists():
                continue

            f_mimetypes = mimetypes.guess_type(f.absolute())[0]

            # f_ext = f.suffix.lower()
            # if not f_ext:
            #     print(f.stem)

            if f_mimetypes and (
                f_mimetypes.startswith("video") or f_mimetypes == "audio/x-pn-realaudio"
            ):
                print(f)
                c += 1
                os.makedirs(f_h264.parent, exist_ok=True)
                subprocess.run(
                    [
                        "ffmpeg",
                        "-i",
                        str(f),
                        "-vcodec",
                        "libx264",
                        "-movflags",
                        "faststart",
                        str(f_h264),
                    ]
                )

                if c >= limit:
                    break

        print(f"convert: {c}")
