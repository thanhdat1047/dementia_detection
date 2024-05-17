# detection/models.py

from django.db import models

class DementiaImage(models.Model):
    image = models.ImageField(upload_to='images/')
    prediction = models.CharField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.image.name
