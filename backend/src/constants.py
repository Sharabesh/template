import os

# Change these for respective os environment variables:
IMAGE_UPLOAD_TAG = "CLOUDINARY_URL"
DATABASE_ENVIRONMENT_VARIABLE = "DATABASE_ENTRY"
COOKIE_SECRET_CODE = "COOKIE_SECRET_VARIABLE"

# Default initialization parameters
DEFAULT_TAG = "WEB_APPLICATION_DEFAULT"
PORT = 5000
Uid = int


assert (
    IMAGE_UPLOAD_TAG in os.environ
), f"Set the cloundinary environment variable \"{IMAGE_UPLOAD_TAG}\" for image uploads"
CLOUDINARY_URL = os.environ[IMAGE_UPLOAD_TAG]


assert (
    DATABASE_ENVIRONMENT_VARIABLE in os.environ
), f"Set the database entry \"{DATABASE_ENVIRONMENT_VARIABLE}\" for global db access"
DATABASE_URL = os.environ[DATABASE_ENVIRONMENT_VARIABLE]

assert (
    COOKIE_SECRET_CODE in os.environ
), f"Set the cookie secret variable \"{COOKIE_SECRET_CODE}\" to a secure random string"
COOKIE_SECRET = os.environ[COOKIE_SECRET_CODE]
