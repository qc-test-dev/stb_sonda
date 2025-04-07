from django import forms
from .models import Document

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
                "type":"file",
            }),
        }
