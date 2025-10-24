import os

# Database
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///products.db')

# Cloudinary
CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', 'your_cloud_name')
API_KEY = os.environ.get('CLOUDINARY_API_KEY', 'your_api_key')
API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', 'your_api_secret')
