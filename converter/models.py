# converter/models.py
from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=50, blank=True, null=True)
    converted_file = models.FileField(upload_to='converted/', blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    file_size = models.CharField(max_length=50, blank=True, null=True)
    output_file_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.file.name
