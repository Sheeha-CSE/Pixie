import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Detect if running in a Serverless / Read-Only environment (Vercel, AWS Lambda)
IS_VERCEL = (
    os.getenv('VERCEL') == '1'
    or os.getenv('VERCEL_ENV') is not None
    or os.getenv('AWS_LAMBDA_FUNCTION_NAME') is not None
)

# Load .env file if present
dotenv_path = BASE_DIR / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'marketmind_ai_default_secret_key_2026')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

    # On Vercel / serverless functions, only /tmp is writable
    if IS_VERCEL:
        DATABASE_PATH = Path('/tmp') / 'marketmind.db'
        UPLOAD_FOLDER = Path('/tmp') / 'uploads'
    else:
        DATABASE_PATH = BASE_DIR / 'marketmind.db'
        UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'

    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 MB max for video/image uploads
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'webm', 'mov'}

    # Default fallback Groq model
    GROQ_MODEL = "llama-3.3-70b-versatile"
    GROQ_FAST_MODEL = "llama-3.1-8b-instant"

# Ensure upload directory exists safely without crashing on read-only environments
try:
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
except Exception:
    Config.UPLOAD_FOLDER = Path('/tmp') / 'uploads'
    try:
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    except Exception:
        pass
