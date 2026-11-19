from urllib.parse import urlparse
from ipaddress import ip_address

from chatamu.exception.custom_exceptions import (
    InvalidURLException
)

def normalize_url(url: str) -> str:

    url = url.strip()
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise InvalidURLException("Unsupported URL scheme")

    if not parsed.hostname:
        raise InvalidURLException("Invalid hostname")

    if parsed.username or parsed.password:
        raise InvalidURLException("URL credentials are not allowed")

    hostname = parsed.hostname.lower().rstrip(".")

    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise InvalidURLException("Localhost URLs are not allowed")

    try:
        ip = ip_address(hostname)
        if not ip.is_global:
            raise InvalidURLException("Private IP addresses are not allowed")
    except ValueError:
        pass

    return url


def is_same_domain(url: str, root_url: str) -> bool:

    target_host = urlparse(url).hostname
    root_host = urlparse(root_url).hostname

    if not target_host or not root_host:
        return False

    target_host = target_host.lower().rstrip(".")
    root_host = root_host.lower().rstrip(".")

    return (
        target_host == root_host
        or target_host.endswith("." + root_host)
    )


def validate_url(url: str, root_url: str) -> bool:

    normalize_url(url)
    normalize_url(root_url)

    if not is_same_domain(url, root_url):
        raise InvalidURLException(
            f"External URL rejected: {url}"
        )

    return True
