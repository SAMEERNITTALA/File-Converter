# converter/forms.py
from django import forms
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    height = forms.IntegerField(required=False, label="Height (px)")
    width = forms.IntegerField(required=False, label="Width (px)")
    file_size = forms.CharField(required=False, label="File Size (e.g., 5MB, 10KB)")
    output_file_name = forms.CharField(required=False, label="Output File Name")

    class Meta:
        model = UploadedFile
        fields = ['file', 'height', 'width', 'file_size', 'output_file_name']