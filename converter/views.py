# converter/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import UploadedFile
import os
from PIL import Image

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
        file_id = request.POST.get('file_id')
        output_file_type = request.POST.get('output_file_type')
        uploaded_file = UploadedFile.objects.get(id=file_id)

        # Perform file conversion
        input_path = uploaded_file.file.path
        output_filename = os.path.splitext(uploaded_file.file.name)[0] + '.' + output_file_type.lower()
        output_path = os.path.join('media/converted/', output_filename)

        if output_file_type in ['jpg', 'jpeg', 'png', 'gif']:
            # Convert image files
            img = Image.open(input_path)
            img.save(output_path, output_file_type.upper())
        else:
            # Handle other file types (e.g., documents)
            # Add your conversion logic here
            pass

        # Serve the converted file for download
        with open(output_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_path)}"'
            return response
    return HttpResponse("Invalid request", status=400)
