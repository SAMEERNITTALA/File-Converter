# converter/views.py
import logging
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import UploadedFile
import os
from PIL import Image

logger = logging.getLogger(__name__)

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            return render(request, 'converter/index.html', {'form': form, 'uploaded_file': uploaded_file})
    else:
        form = UploadFileForm()
    return render(request, 'converter/index.html', {'form': form})

def convert_file(request):
    if request.method == 'POST':
        try:
            # Log the incoming request data
            logger.info(f"Incoming request data: {request.POST}")
            logger.info(f"Files in request: {request.FILES}")

            # Get the uploaded file
            uploaded_file = request.FILES.get('files')
            if not uploaded_file:
                logger.error("No file uploaded.")
                return HttpResponse("No file uploaded.", status=400)

            # Get the output file type
            output_file_type = request.POST.get('output_file_type')
            if not output_file_type:
                logger.error("Output file type not specified.")
                return HttpResponse("Output file type not specified.", status=400)

            # Perform file conversion
            input_path = f"media/uploads/{uploaded_file.name}"
            output_filename = os.path.splitext(uploaded_file.name)[0] + '.' + output_file_type.lower()
            output_path = os.path.join('media/converted/', output_filename)

            # Save the uploaded file temporarily
            with open(input_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Convert the file
            if output_file_type.lower() in ['jpg', 'jpeg', 'png', 'gif']:
                img = Image.open(input_path)
                img.save(output_path, output_file_type.upper())
            else:
                logger.error(f"Unsupported output file type: {output_file_type}")
                return HttpResponse(f"Unsupported output file type: {output_file_type}", status=400)

            # Serve the converted file for download
            with open(output_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_path)}"'
                return response

        except Exception as e:
            logger.error(f"Error during file conversion: {str(e)}")
            return HttpResponse(f"File conversion failed: {str(e)}", status=500)

    return HttpResponse("Invalid request", status=400)
