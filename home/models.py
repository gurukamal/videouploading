from django.db import models
from .validators import file_size

# Create your models here.

class Video(models.Model):
    title=models.CharField(max_length=100,null=True,blank=True)
    video=models.FileField(upload_to="video/%y",validators=[file_size])
    subtitle_file = models.FileField(upload_to='subtitles/', null=True, blank=True)
    subtitle_content = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=50, default="en")  # Subtitle language
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title