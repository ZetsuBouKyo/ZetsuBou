from urllib.parse import urlparse


def get_host(url: str, endswith_slash: bool = False) -> str:
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    hostname = parsed_url.hostname
    port = parsed_url.port
    if not scheme:
        raise ValueError("scheme not found")
    if not hostname:
        raise ValueError("hostname not found")

    host = f"{scheme}://{hostname}"

    if port is not None:
        host += f":{port}"

    if endswith_slash:
        host += "/"
    return host
