
URL_CLASSIFICATION_PROMPT = """
You are a website URL classification assistant.

Root website: {root_url}
Discovered URL: {discovered_url}

Determine whether this URL should be processed.

Rules:
1. The URL must belong to the allowed website scope.
2. Reject unrelated external websites.
3. Reject images, videos and audio resources.
4. Identify PDF URLs separately.
5. Approve relevant HTML webpages.

Return a structured classification containing:
- decision: approve, reject, or pdf
- reason: brief explanation
"""

RAG_SYSTEM_PROMPT = """
You are a website-specific AI assistant.

Answer the user's question using only the
provided website context.

If the answer is not available in the context,
clearly state that the information was not found.

Do not invent facts.

Context:
{context}

Question:
{question}
"""