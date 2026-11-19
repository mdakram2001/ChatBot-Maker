from fastapi import FastAPI

from chatamu.api.routes import website, chatbot

app = FastAPI(
    title="ChatAMU API",
    description="Website-based RAG chatbot API",
    version="1.0.0",
)



app.include_router(website.router)
app.include_router(chatbot.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to ChatAMU API",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}