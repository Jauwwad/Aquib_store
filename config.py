import os
from dotenv import load_dotenv

load_dotenv()

# Database connection (Render or Neon DB)
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

# Cloudinary configuration
CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
API_KEY = os.getenv("CLOUDINARY_API_KEY")
API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
