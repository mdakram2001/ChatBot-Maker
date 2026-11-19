
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from chatamu.entity.url import URLInfo
from chatamu.core.url_validator import normalize_url


def discover_urls(html: str, source_url: str) -> list[URLInfo]:

    soup = BeautifulSoup(html, "html.parser")

    discovered = []
    visited = set()

    for link in soup.find_all("a", href=True):

        href = link["href"].strip()

        try:
            absolute_url = urljoin(source_url, href)

            absolute_url = normalize_url(absolute_url)

            if absolute_url in visited:
                continue

            visited.add(absolute_url)

            discovered.append(
                URLInfo(
                    url=absolute_url,
                    source_url=source_url,
                    anchor_text=link.get_text(strip=True)
                )
            )

        except Exception:
            continue

    return discovered
