# converter/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import UploadedFile
from .ai_file_identification import identify_file_type, get_supported_conversions
from .file_conversion import convert_file
import os

def index(request):
    if request.method == 'POST':
        if 'upload' in request.POST:  # Handle file upload
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = form.save(commit=False)
                uploaded_file.file_type = identify_file_type(uploaded_file.file.path)
                uploaded_file.save()

                # Get supported conversions for the file type
                supported_conversions = get_supported_conversions(uploaded_file.file_type)
                form = UploadFileForm(output_file_types=supported_conversions)
                return render(request, 'converter/index.html', {'form': form, 'uploaded_file': uploaded_file})

        elif 'convert' in request.POST:  # Handle file conversion
            file_id = request.POST.get('file_id')
            uploaded_file = UploadedFile.objects.get(id=file_id)
            uploaded_file.height = request.POST.get('height')
            uploaded_file.width = request.POST.get('width')
            uploaded_file.file_size = request.POST.get('file_size')
            uploaded_file.output_file_name = request.POST.get('output_file_name')
            uploaded_file.output_file_type = request.POST.get('output_file_type')
            uploaded_file.save()

            # Perform file conversion
            converted_file_path = convert_file(
                uploaded_file.file.path,
                uploaded_file.output_file_type,
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
