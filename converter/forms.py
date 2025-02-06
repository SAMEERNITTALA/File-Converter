# converter/forms.py
from django import forms
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    height = forms.IntegerField(required=False, label="Height (px)")
    width = forms.IntegerField(required=False, label="Width (px)")
    file_size = forms.CharField(required=False, label="File Size (e.g., 5MB, 10KB)")
    output_file_name = forms.CharField(required=False, label="Output File Name")
    output_file_type = forms.ChoiceField(choices=[], label="Output File Type")

    class Meta:
        model = UploadedFile
        fields = ['file', 'height', 'width', 'file_size', 'output_file_name', 'output_file_type']

    def __init__(self, *args, **kwargs):
        output_file_types = kwargs.pop('output_file_types', [])
        super().__init__(*args, **kwargs)
        self.fields['output_file_type'].choices = output_file_types