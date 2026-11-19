
from pydantic import BaseModel
from typing import Literal


class URLClassification(BaseModel):

    url: str

    decision: Literal[
        "approve",
        "reject",
        "pdf"
    ]

    url_type: Literal[
        "webpage",
        "pdf",
        "image",
        "video",
        "audio",
        "other"
    ]

    reason: str
