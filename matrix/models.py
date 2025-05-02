# models.py
from django.db import models
class SuperMatriz(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Matriz(models.Model):
    super_matriz = models.ForeignKey(SuperMatriz, on_delete=models.CASCADE, related_name='matrices')
    nombre = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class CasoDePrueba(models.Model):
    CRITICIDAD_CHOICES = [
        ('Bloqueante', 'Bloqueante'),
        ('Crítico', 'Crítico'),
    ]

    matriz = models.ForeignKey(Matriz, on_delete=models.CASCADE, related_name='casos')
    alcance = models.CharField(max_length=5)
    fase = models.CharField(max_length=50)
    caso_de_prueba = models.TextField()
    estado = models.CharField(max_length=50, default="Por ejecutar")
    criticidad = models.CharField(max_length=15, choices=CRITICIDAD_CHOICES)
    nota = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fase} - {self.caso_de_prueba[:30]}..."
