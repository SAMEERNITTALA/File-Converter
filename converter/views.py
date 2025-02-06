# converter/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import UploadedFile
from .ai_file_identification import identify_file_type
from .file_conversion import convert_file
import os

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.file_type = identify_file_type(uploaded_file.file.path)
            uploaded_file.save()

            # Perform file conversion
            converted_file_path = convert_file(
                uploaded_file.file.path,
                uploaded_file.height,
                uploaded_file.width,
                uploaded_file.file_size,
                uploaded_file.output_file_name
            )

            # Update the model with the converted file
            uploaded_file.converted_file.name = converted_file_path
            uploaded_file.save()

            # Trigger automatic download
            response = HttpResponse(uploaded_file.converted_file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(converted_file_path)}"'
            return response
    else:
        form = UploadFileForm()
    return render(request, 'converter/index.html', {'form': form})
