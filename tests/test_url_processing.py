
import pytest

from chatamu.core.url_validator import (
    validate_url,
    is_same_domain
)

from chatamu.core.url_discovery import discover_urls

from chatamu.exception.custom_exceptions import (
    InvalidURLException
)


def test_same_domain():

    assert is_same_domain(
        "https://example.com/about",
        "https://example.com"
    )


def test_subdomain():

    assert is_same_domain(
        "https://blog.example.com",
        "https://example.com"
    )


def test_external_domain():

    assert not is_same_domain(
        "https://google.com",
        "https://example.com"
    )


def test_invalid_scheme():

    with pytest.raises(InvalidURLException):
        validate_url(
            "ftp://example.com",
            "https://example.com"
        )


def test_url_discovery():

    html = """
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
    <a href="/about">About Again</a>
    """

    urls = discover_urls(
        html,
        "https://example.com"
    )

    assert len(urls) == 2
