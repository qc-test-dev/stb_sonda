# forms.py
from django import forms
from .models import SuperMatriz, Matriz, CasoDePrueba

class MatrizForm(forms.ModelForm):
    class Meta:
        model = Matriz
        fields = ['nombre']  # Incluye los campos que quieres que el usuario pueda llenar
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
class CasoDePruebaForm(forms.ModelForm):
    ESTADO_CHOICES = [
        ('funciona', 'Funciona'),
        ('falla_nueva', 'Falla nueva'),
        ('falla_persistente', 'Falla persistente'),
        ('na', 'N/A'),
        ('pendiente', 'Pendiente'),
        ('por_ejecutar', 'Por ejecutar'),
    ]

    estado = forms.ChoiceField(
    choices=ESTADO_CHOICES,
    widget=forms.Select(attrs={
        'class': 'form-select estado-select'
    })
)

    nota = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'style': 'resize: none;'
        }),
        required=False
    )

    class Meta:
        model = CasoDePrueba
        fields = ['estado', 'nota']
class SuperMatrizForm(forms.ModelForm):
    class Meta:
        model = SuperMatriz
        fields = ['nombre', 'descripcion']

    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))