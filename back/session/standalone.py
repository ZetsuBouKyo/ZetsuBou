# deprecated

import httpx
from back.settings import setting
from fastapi.responses import RedirectResponse

standalone_url = setting.standalone_url


class StandaloneSession:
    def __init__(self, standalone_url: str = standalone_url):
        self.standalone_url = standalone_url

    def open_folder(self, gallery_id: str):
        return RedirectResponse(
            url=f"{self.standalone_url}/open?gallery_id={gallery_id}"
        )

    def sync_new(self):
        return RedirectResponse(url=f"{self.standalone_url}/sync-new-galleries")

    def ping(self):
        url = f"{self.standalone_url}/ping"
        resp = httpx.get(url)
        if resp.status_code == 200:
            return True

        return False


standalone_client = StandaloneSession()
