from django import forms
from .models import Apk

class APKForm(forms.ModelForm):
    class Meta:
        model = Apk
        fields = ["title", "document"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "id": "document-title",
                "placeholder": "Apk 1.0.0"
            }),
            "document": forms.ClearableFileInput(attrs={
                "class": "form-file",
                "id": "document-file",
                "type":"file",
            }),
        }
