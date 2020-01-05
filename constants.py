import os

DEFAULT_TAG = "WEB_APPLICATION_DEFAULT"


assert "CLOUDINARY_URL" in os.environ, "Set the cloundinary environment variable for image uploads"
CLOUDINARY_URL = os.environ['cloudinary_url']

