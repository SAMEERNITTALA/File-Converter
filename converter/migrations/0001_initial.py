# Generated by Django 5.0.6 on 2025-02-06 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('file_type', models.CharField(blank=True, max_length=50, null=True)),
                ('converted_file', models.FileField(blank=True, null=True, upload_to='converted/')),
                ('height', models.IntegerField(blank=True, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('file_size', models.CharField(blank=True, max_length=50, null=True)),
                ('output_file_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
