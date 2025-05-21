from django import forms
from .models import Apk
from django.core.exceptions import ValidationError
import os
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
                "accept": ".apk",
            }),
            
        }
def clean_document(self):
        document = self.cleaned_data.get('document')

        # Verificar si el archivo tiene una extensión válida
        valid_extensions = ['.apk']
        ext = os.path.splitext(document.name)[1].lower()

        if ext not in valid_extensions:
            raise ValidationError('Solo se permiten archivos .txt, .pdf y .docx.')

        return document
