from django import forms
from .models import SuperMatriz, Matriz, CasoDePrueba, Validate, TicketPorLevantar, DetallesValidate

# Listas de opciones
ALCANCE_CHOICES = [
    ('A', 'MVP (A)'),
    ('A,B', 'SMOKE TEST (A,B)'),
    ('A,B,C', 'NA (A,B,C)'),
]
TESTERS = [
    ('Kevin', 'Kevin'),
    ('Erik', 'Erik'),
    ('Kyle', 'Kyle'),
    ('Alberto', 'Alberto'),
    ('Axel', 'Axel'),
    ('Luis Rene', 'Luis Rene'),
]
REGIONES = [
    ('Peru', 'Peru'),
    ('Argentina', 'Argentina'),
    ('Dominicana', 'Dominicana'),
    ('Guatemala', 'Guatemala'),
    ('Panama', 'Panama'),
]
Prioridad_CHOICES = [
    ('Bloqueante', 'Bloqueante'),
    ('Crítico', 'Crítico'),
]

# Formularios

class SuperMatrizForm(forms.ModelForm):
    class Meta:
        model = SuperMatriz
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': '100'}),
        }


class MatrizForm(forms.ModelForm):
    alcance = forms.ChoiceField(
        choices=ALCANCE_CHOICES,
        widget=forms.RadioSelect,
        label='Alcance Evaluación',
        required=True
    )
    testers = forms.MultipleChoiceField(
        choices=TESTERS,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Testers"
    )
    regiones = forms.MultipleChoiceField(
        choices=REGIONES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Regiones"
    )

    class Meta:
        model = Matriz
        fields = ['nombre', 'alcance']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
        }


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
        widget=forms.Select(attrs={'class': 'form-select estado-select'})
    )

    nota = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'style': 'resize: none;',
            'maxlength': '1000'  # Aproximado si no definido
        }),
        required=False
    )

    class Meta:
        model = CasoDePrueba
        fields = ['estado', 'nota']


class ValidateForm(forms.ModelForm):
    class Meta:
        model = Validate
        exclude = ['super_matriz']
        widgets = {
            'tester': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'ticket': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prioridad': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
        }


class ValidateEstadoForm(forms.ModelForm):
    class Meta:
        model = Validate
        fields = ['estado']
        widgets = {
            'estado': forms.Select(choices=[
                ('funciona', 'Funciona'),
                ('falla_nueva', 'Falla Nueva'),
                ('falla_persistente', 'Falla Persistente'),
                ('na', 'N/A'),
                ('pendiente', 'Pendiente'),
                ('por_ejecutar', 'Por Ejecutar')
            ], attrs={'class': 'form-select estado-select', 'maxlength': '50'})
        }


class TicketPorLevantarForm(forms.ModelForm):
    tester = forms.ChoiceField(choices=TESTERS, widget=forms.Select(attrs={'class': 'form-select'}))
    Region = forms.ChoiceField(choices=REGIONES, widget=forms.Select(attrs={'class': 'form-select'}))
    prioridad = forms.ChoiceField(choices=Prioridad_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = TicketPorLevantar
        fields = ['tester', 'ticket_SCT', 'BRF', 'Region', 'prioridad', 'desc', 'nota', 'url']
        widgets = {
            'ticket_SCT': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'BRF': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '30'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'maxlength': '70'}),
            'nota': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'maxlength': '70'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class DetallesValidateForm(forms.ModelForm):
    class Meta:
        model = DetallesValidate
        fields = ['filtro_RN', 'comentario_RN']
        widgets = {
            'filtro_RN': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '150',
                'placeholder': 'Escribe el filtro aplicado por RN...'
            }),
            'comentario_RN': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'style': 'resize: none;',
                'maxlength': '150',
                'placeholder': 'Agrega aquí los labels de RN'
            }),
        }
