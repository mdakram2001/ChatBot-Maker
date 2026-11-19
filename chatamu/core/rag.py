
from langchain_openai import ChatOpenAI

from chatamu.config.settings import settings
from chatamu.services.vector_service import search_documents
from chatamu.constants.prompt_constants import RAG_SYSTEM_PROMPT

from chatamu.logger.logging_config import logger

def get_llm():

    return ChatOpenAI(
        model=settings.LLM_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        api_key=settings.OLLAMA_API_KEY,
        temperature=0
    )

def ask_question(question: str, top_k: int = 5):

    logger.info(f"Processing question: {question}")

    # Retrieve relevant documents
    results = search_documents(
        question,
        top_k=top_k
    )

    documents = results.get("documents", [[]])[0]

    if not documents:
        return "No relevant information found on this website."

    # Prepare context
    context = "\n\n".join(documents)

    # Prepare prompt
    prompt = RAG_SYSTEM_PROMPT.format(
        context=context,
        question=question
    )

    # Generate answer
    llm = get_llm()

    response = llm.invoke(prompt)

    return response.content