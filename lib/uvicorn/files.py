from collections import deque
from pathlib import Path
from typing import List

from pydantic import BaseModel

from back.logging import logger_zetsubou


class PathPattern(BaseModel):
    pattern: str
    left: bool


def _get_both_side_patterns(patterns: List[str]) -> List[PathPattern]:
    return [PathPattern(pattern=p, left=True) for p in patterns]


def _get_patterns(patterns: List[str]) -> List[PathPattern]:
    return [PathPattern(pattern=p, left=False) for p in patterns]


excludes = _get_both_side_patterns(
    [
        "__pycache__",
        ".git",
        ".pytest_cache",
        ".venv",
        ".pytest_cache",
        "node_modules",
    ]
) + _get_patterns(
    [
        ".python-version",
        ".vscode" "*.code-workspace",
        "*.db",
        "dev",
        "front",
        "logs",
        "package-lock.json",
        "poetry.lock*",
        "target",
    ]
)

includes = ["front/dist", "front/doc_site", "front/public"]


def get_watched_files(
    home: Path = Path.cwd(), excludes: List[PathPattern] = excludes
) -> List[Path]:
    watched = []
    stack = deque([p for p in home.glob("*")])
    while stack:
        skip = False
        p = stack.popleft()
        relative_p = p.relative_to(home)
        for ignore in excludes:
            if not ignore.left:
                first_path = Path(relative_p.parts[0])
                if first_path.match(ignore.pattern):
                    skip = True
                    continue
            elif relative_p.name == ignore.pattern:
                skip = True
                continue
        if skip:
            continue

        if p.is_dir():
            for next_p in p.glob("*"):
                stack.append(next_p)
            continue

        watched.append(p)

    for include in includes:
        p = home / include
        for next_p in p.glob("**/*"):
            watched.append(next_p)
    logger_zetsubou.info(f"watched files: {len(watched)}")
    return watched
