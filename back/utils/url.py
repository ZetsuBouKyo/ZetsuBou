from urllib.parse import urlparse


def get_host(url: str, endswith_slash: bool = False) -> str:
    parsed_url = urlparse(url)
    host = f"{parsed_url.scheme}://{parsed_url.hostname}:{parsed_url.port}"
    if endswith_slash:
        host += "/"
    return host
