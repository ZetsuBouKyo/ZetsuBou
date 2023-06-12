import os
from pathlib import Path

import httpx

STATICS_HOME = "./statics"


async def get_static_file(url: str, statics_home: str = STATICS_HOME):
    os.makedirs(statics_home, exist_ok=True)
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
    filename = Path(url).name
    filepath = Path(statics_home) / filename
    with filepath.open(mode="w") as fp:
        fp.write(resp.text)
