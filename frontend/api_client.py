import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def create_website(url: str) -> dict:
    """Submit a website for crawling and indexing."""

    response = requests.post(
        f"{API_BASE_URL}/website/create",
        json={"url": url},
        timeout=600,
    )

    response.raise_for_status()
    return response.json()


def ask_question(question: str, top_k: int = 4) -> dict:
    """Send a question to the ChatAMU RAG API."""

    response = requests.post(
        f"{API_BASE_URL}/chat/",
        json={
            "question": question,
            "top_k": top_k,
        },
        timeout=120,
    )

    response.raise_for_status()
    return response.json()