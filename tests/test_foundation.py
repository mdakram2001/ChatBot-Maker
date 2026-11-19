from chatamu.config.settings import settings
from chatamu.logger.logging_config import logger
from chatamu.exception.custom_exceptions import (
    InvalidURLException
)

def test_settings():
    assert settings.APP_NAME == "ChatAMU"
    assert settings.MAX_PAGES > 0

def test_logger():
    assert logger is not None

def test_custom_exception():
    try:
        raise InvalidURLException("Invalid URL")

    except InvalidURLException as e:
        assert str(e) == "Invalid URL"