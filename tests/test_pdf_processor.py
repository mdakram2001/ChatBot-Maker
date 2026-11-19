
from unittest.mock import patch, Mock

import pytest

from chatamu.core.pdf_processor import extract_pdf
from chatamu.exception.custom_exceptions import (
    PDFExtractionException
)


def test_invalid_pdf():

    mock_response = Mock()

    mock_response.headers = {
        "Content-Type": "text/html"
    }

    mock_response.content = b"<html>Not a PDF</html>"

    mock_response.raise_for_status.return_value = None

    with patch(
        "chatamu.core.pdf_processor.requests.get",
        return_value=mock_response
    ):

        with pytest.raises(PDFExtractionException):
            extract_pdf("https://example.com/file.pdf")
