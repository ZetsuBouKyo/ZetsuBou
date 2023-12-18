from collections import deque
from pathlib import Path
from typing import List

from back.logging import logger_zetsubou

excludes = [
    "__pycache__",
    ".git",
    ".pytest_cache",
    ".venv",
    "node_modules",
]

root_excludes = [
    ".python-version",
    ".vscode",
    "*.code-workspace",
    "*.db",
    "dev",
    "front",
    "logs",
    "package-lock.json",
    "poetry.lock*",
    "target",
]

root_excludes += excludes


includes = ["front/dist", "front/doc_site", "front/public"]


def get_watched_files(
    home: Path = Path.cwd(),
    root_excludes: List[str] = root_excludes,
    excludes: List[str] = excludes,
    includes: List[str] = includes,
) -> List[Path]:
    watched = []
    stack = deque([])
    for p in home.glob("*"):
        relative_p = p.relative_to(home)
        first_path = Path(relative_p.parts[0])

        skip = False
        for ignore in root_excludes:
            if first_path.match(ignore):
                skip = True
                break
        if skip:
            continue

        stack.append(p)

    for include in includes:
        p = home / include
        stack.append(p)

    while stack:
        skip = False
        p = stack.popleft()
        relative_p = p.relative_to(home)
        for ignore in excludes:
            if relative_p.name == ignore:
                skip = True
                break
        if skip:
            continue

        if p.is_dir():
            for next_p in p.glob("*"):
                stack.append(next_p)
            continue

        watched.append(p)

    logger_zetsubou.info(f"watched files: {len(watched)}")
    return watched


def check_files(cwd: Path, files: List[str]) -> bool:
    for f in files:
        relative_f = f.relative_to(cwd)
        for i, part in enumerate(relative_f.parts):
            if i == 0:
                if len(relative_f.parts) > 1:
                    p = Path(part) / relative_f.parts[1]
                    p = str(p)
                    if p in includes:
                        continue
                for exclude in root_excludes:
                    assert not Path(part).match(
                        exclude
                    ), f"`{relative_f}` should not be included."
            assert part not in excludes, f"`{relative_f}` should not be included."
    return True
