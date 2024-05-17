# detection/forms.py

from django import forms
from .models import DementiaImage

class DementiaImageForm(forms.ModelForm):
    class Meta:
        model = DementiaImage
        fields = ['image']
