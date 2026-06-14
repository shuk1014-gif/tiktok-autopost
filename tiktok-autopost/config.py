import os
from dotenv import load_dotenv

load_dotenv()

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")
FAL_KEY = os.getenv("FAL_KEY", "")
X_API_KEY = os.getenv("X_API_KEY", "")
X_API_SECRET = os.getenv("X_API_SECRET", "")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN", "")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET", "")
TIKTOK_CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY", "")
TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET", "")
TIKTOK_REDIRECT_URI = os.getenv("TIKTOK_REDIRECT_URI", "http://localhost:8080/callback")
TIKTOK_PRIVACY = os.getenv("TIKTOK_PRIVACY", "SELF_ONLY")

POST_TIMES = os.getenv("POST_TIMES", "07:00,20:00").split(",")

OUTPUT_DIR = "output"
MUSIC_DIR = "music"
TOKEN_FILE = ".tiktok_token.json"
LOG_FILE = "autopost.log"

STABILITY_IMAGE_MODEL = "stable-diffusion-xl-1024-v1-0"
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
