# This is a function-based view, which is simple and perfect for a single action.

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from app.models import Uploads

# from .models import Uploads

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Protect the endpoint
def download_file_view(request, file_id):
    """
    Finds a file by its ID and returns it as a download.
    This corresponds to `UploadsController@download_file`.
    """
    # get_object_or_404 is a robust way to find the record or return a 404 error.
    upload = get_object_or_404(Uploads, pk=file_id)

    try:
        # The `path.open()` method opens the file from your storage backend.
        # `FileResponse` streams the file efficiently, which is great for large files.
        # `as_attachment=True` tells the browser to prompt for download.
        response = FileResponse(upload.path.open('rb'), as_attachment=True)
        return response
    except FileNotFoundError:
        # This handles cases where the database record exists but the file is missing.
        raise Http404("File not found on the server.")
    except Exception as e:
        # Catch other potential errors
        return response({"error": f"An error occurred: {str(e)}"}, status=500)