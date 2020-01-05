from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import os
import sys
from constants import DEFAULT_TAG, CLOUDINARY_URL


if not os.environ.get("CLOUDINARY_URL"):
    raise Exception("Need to have access to image server. Please set Cloudinary URL")


async def upload_file() -> str:
    """
    This method takes a binary stream of data writes it to a local file
    and then uses the native upload method to upload this image to our hosting server.
    We then clean up the temporary file on the local server.
    TODO: There may be a possibility to upload directly though it doesn't seem like cloundary supports that for the moment
    """

    response = upload(
        # Upload and auto resize image into a nice size (keep storage small)
        "data/tmp.jpeg",
        tags=DEFAULT_TAG,
        eager=dict(width=250, height=250, crop="scale"),
        eager_async=True,
    )
    os.remove("data/tmp.jpeg")
    return response["secure_url"]
