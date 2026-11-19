
class ChatAMUException(Exception):
    """Base exception for ChatAMU."""
    pass

class InvalidURLException(ChatAMUException):
    """Raised when the supplied URL is invalid."""
    pass

class WebsiteAccessException(ChatAMUException):
    """Raised when a website cannot be accessed."""
    pass

class URLClassificationException(ChatAMUException):
    """Raised when URL classification fails."""
    pass

class WebExtractionException(ChatAMUException):
    """Raised when webpage extraction fails."""
    pass

class PDFExtractionException(ChatAMUException):
    """Raised when PDF extraction fails."""
    pass

class EmbeddingException(ChatAMUException):
    """Raised when embedding generation fails."""
    pass

class VectorDatabaseException(ChatAMUException):
    """Raised when vector database operations fail."""
    pass

class LLMException(ChatAMUException):
    """Raised when LLM operations fail."""
    pass