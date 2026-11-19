from fastapi import APIRouter, HTTPException

from chatamu.api.schemas.website_schema import (
    WebsiteCreateRequest,
    WebsiteCreateResponse,
)
from chatamu.services.crawler_service import start_crawl
from chatamu.services.pdf_service import process_pdf_urls
from chatamu.services.vector_service import index_documents

router = APIRouter(prefix="/website", tags=["Website"])

# Initial prototype: one website per running application.
active_website_url: str | None = None


@router.post("/create", response_model=WebsiteCreateResponse)
def create_website(request: WebsiteCreateRequest):
    global active_website_url

    website_url = str(request.url)

    if active_website_url is not None:
        raise HTTPException(
            status_code=409,
            detail=(
                "A website has already been indexed in this application. "
                "Multi-website isolation will be added in a later phase."
            ),
        )

    try:
        # Step 1: Crawl website pages
        crawl_result = start_crawl(website_url)

        summary = crawl_result["summary"]
        web_documents = crawl_result["documents"]

        # Step 2: Process discovered PDFs
        pdf_result = process_pdf_urls(summary.pdf_urls)
        pdf_documents = pdf_result["documents"]

        # Step 3: Combine documents
        all_documents = web_documents + pdf_documents

        if not all_documents:
            raise HTTPException(
                status_code=422,
                detail="No content could be extracted from this website.",
            )

        # Step 4: Generate embeddings and store in ChromaDB
        index_result = index_documents(all_documents)

        active_website_url = website_url

        return WebsiteCreateResponse(
            website_url=website_url,
            status="completed",
            web_pages_processed=summary.pages_processed,
            pdfs_processed=pdf_result["processed_count"],
            chunks_indexed=index_result["chunks_indexed"],
            message="Website content successfully indexed.",
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Website processing failed: {str(exc)}",
        ) from exc