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
    alcances_utilizados = models.CharField(max_length=100, blank=True, null=True)

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
    tester=models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fase} - {self.caso_de_prueba[:30]}..."
class Validate(models.Model):
    super_matriz = models.ForeignKey(SuperMatriz, on_delete=models.CASCADE, related_name='validates')
    matriz = models.ForeignKey(Matriz, on_delete=models.CASCADE, related_name='validates', null=True, blank=True)
    tester = models.CharField(max_length=255, null=True, blank=True)
    ticket = models.CharField(max_length=100,null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    prioridad = models.CharField(max_length=50,null=True, blank=True)
    estado = models.CharField(max_length=50,null=True, blank=True)

    def __str__(self):
        ticket_url = f"https://dlatvarg.atlassian.net/browse/{self.ticket}" if self.ticket else "Sin Ticket"
        return f"{self.tester} — <a href='{ticket_url}' target='_blank'>{ticket_url}</a>"


class TicketPorLevantar(models.Model):
    super_matriz = models.ForeignKey(SuperMatriz, on_delete=models.CASCADE, related_name='tickets_por_levantar')
    tester = models.CharField(max_length=100)
    ticket_SCT = models.CharField(max_length=10,blank=True,null=True)
    BRF = models.CharField(max_length=30,blank=True,null=True)
    Region = models.CharField(max_length=100)
    desc = models.TextField(max_length=70)
    prioridad = models.CharField(max_length=50)
    nota = models.TextField(max_length=70)
    url = models.URLField(null=True,blank=True)

    def __str__(self):
        return f"{self.tester} - {self.ticket_SCT}"
class DetallesValidate(models.Model):
    super_matriz = models.OneToOneField(SuperMatriz, on_delete=models.CASCADE, related_name='detalles_validate')   
    filtro_RN = models.CharField(max_length=255,blank=True, null=True)
    comentario_RN = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Detalles de {self.super_matriz.nombre}"

    
    


