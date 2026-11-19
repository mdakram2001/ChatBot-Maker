
# Supported URL schemes
ALLOWED_SCHEMES = ("http", "https")

# Resource extensions
IMAGE_EXTENSIONS = (
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"
)

VIDEO_EXTENSIONS = (
    ".mp4", ".avi", ".mov", ".webm", ".mkv"
)

AUDIO_EXTENSIONS = (
    ".mp3", ".wav", ".ogg", ".m4a"
)

PDF_EXTENSIONS = (".pdf",)

# URL types
URL_TYPE_WEBPAGE = "webpage"
URL_TYPE_PDF = "pdf"
URL_TYPE_IMAGE = "image"
URL_TYPE_VIDEO = "video"
URL_TYPE_AUDIO = "audio"
URL_TYPE_OTHER = "other"