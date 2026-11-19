from dataclasses import dataclass

@dataclass
class URLInfo:
    url: str
    source_url: str
    anchor_text: str = ""
    url_type: str = "unknown"
    status: str = "discovered"
