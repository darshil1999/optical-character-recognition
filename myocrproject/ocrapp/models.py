from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class registerUser(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=120)

    def __str__(self):
        return self.username

class uploadedFile(models.Model):
    file_name = models.CharField(max_length=255, help_text="The name of the file.")
    image_data = models.BinaryField()
    file_path = models.CharField(max_length=1024, help_text="The path to the file.")
    uploaded_at = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.file_name


class ProcessedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='result/%Y/%m/%d/')  
    image_data = models.BinaryField(null=True, blank=True)
    processed_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
