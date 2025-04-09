from django import forms
from .models import Document
from django.core.exceptions import ValidationError
import os
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "description", "document"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "id": "document-title",
                "placeholder": "Título del documento"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-textarea",
                "id": "document-description",
                "rows": 4,
                "cols": 40,
                "placeholder": "Escribe una breve descripción..."
            }),
            "document": forms.ClearableFileInput(attrs={
                "class": "form-file",
                "id": "document-file",
                "type": "file",
                "accept": ".txt, .pdf, .docx",  # Limita los tipos de archivo
            }),
        }

def clean_document(self):
        document = self.cleaned_data.get('document')

        # Verificar si el archivo tiene una extensión válida
        valid_extensions = ['.txt', '.pdf', '.docx']
        ext = os.path.splitext(document.name)[1].lower()

        if ext not in valid_extensions:
            raise ValidationError('Solo se permiten archivos .txt, .pdf y .docx.')

        return document