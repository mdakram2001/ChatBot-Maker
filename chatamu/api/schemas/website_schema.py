from pydantic import BaseModel, HttpUrl, Field


class WebsiteCreateRequest(BaseModel):
    url: HttpUrl


class WebsiteCreateResponse(BaseModel):
    website_url: str
    status: str
    web_pages_processed: int
    pdfs_processed: int
    chunks_indexed: int
    message: str