# converter/views.py
from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadedFile

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = UploadFileForm()
    return render(request, 'converter/index.html', {'form': form})
