from fastapi import status
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

# Load environment variables
load_dotenv()
IMAGEKIT_PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")
IMAGEKIT_PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
IMAGEKIT_URL_ENDPOINT = os.getenv("IMAGEKIT_URL_ENDPOINT")

# Initialize ImageKit instance
imagekit = ImageKit(
    private_key=IMAGEKIT_PRIVATE_KEY,
    public_key=IMAGEKIT_PUBLIC_KEY,
    url_endpoint=IMAGEKIT_URL_ENDPOINT,
)

def upload_to_imagekit(file, file_name="uploaded-file.jpg"):
    """
    Uploads a file to ImageKit. Supports URL, Base64, or Binary formats.
    :param file: File content (URL, Base64 string, or Binary object).
    :param file_name: Name of the file to be uploaded.
    :return: Result dictionary with status and details.
    """
    try:
        # Define common options
        options = UploadFileRequestOptions(
            use_unique_file_name=True,
            tags=['upload', 'user'],
            folder='/testing-folder/',
            is_private_file=False,
            response_fields=['tags', 'is_private_file'],
            
        )

        # Upload file
        upload = imagekit.upload_file(
            file=file,
            file_name=file_name,
            options=options
        )
            # Extract and return response attributes
        if hasattr(upload, 'response') and upload.response_metadata:
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={"status_code":status.HTTP_201_CREATED, "message": "File uploaded successfully.", "file_id": upload.file_id})
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status_code":status.HTTP_400_BAD_REQUEST, "message": "Failed to upload file."})
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status_code":status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "Internal server error."})


def delete_image_from_imagekit(file_id):
    """
    Deletes an image from ImageKit by its file ID.
    :param file_id: File ID of the image to be deleted.
    :return: Result dictionary with status and details.
    """
    try:
        # Delete file
        delete = imagekit.delete_file(file_id)

        if hasattr(delete, 'response') and delete.response_metadata:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"status_code":status.HTTP_200_OK, "message": "File deleted successfully."})
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status_code":status.HTTP_400_BAD_REQUEST, "message": "Failed to delete file."})
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status_code":status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "Internal server error."})


















#this code is for the V2 of imagekit

def generate_signature(expire, token):
    """
    Generate a signature using the private API key, expiration time, and token.
    :param expire: Expiration timestamp.
    :param token: Unique token for the request.
    :return: Signature string.
    """
    signature = hmac.new(
        IMAGEKIT_PRIVATE_KEY.encode('utf-8'),
        (token + expire).encode('utf-8'),
        hashlib.sha1
    ).hexdigest().lower()
    return signature

def upload_file_via_api(file_obj=None, file_source=None, file_path=None):
    """
    Uploads a file to ImageKit using their API directly.
    :param file_obj: File-like object (binary).
    :param file_source: URL of the file.
    :param file_path: Path to the local file.
    :return: Result dictionary with status and details.
    """
    try:
        # Prepare the upload parameters
        expire_time = str(int(time.time()) + 60)  # Signature expiry time (1 minute)
        token = str(uuid.uuid4())  # Generate a unique token
        signature = generate_signature(expire_time, token)

        files = {
            'file': file_obj if file_obj else open(file_path, 'rb') if file_path else requests.get(file_source).content,
        }

        data = {
            'fileName': 'uploaded-file.jpg',
            'publicKey': IMAGEKIT_PUBLIC_KEY,
            'signature': signature,
            'expire': expire_time,
            'token': token,
            'useUniqueFileName': 'true',
            'tags': 'example,upload',
            'folder': '/uploads/',
            'isPrivateFile': 'false',
            'isPublished': 'true',
        }

        # Make the POST request to upload the file
        response = requests.post(IMAGEKIT_URL, files=files, data=data)

        # Check for response and handle success or failure
        response_data = response.json()
        if response.status_code == 200:
            return {"status": "success", "file_url": response_data.get("url")}
        else:
            return {"status": "error", "message": response_data.get("message", "Unknown error")}
    except Exception as e:
        return {"status": "error", "message": str(e)}


