from django.db import models

# Create your models here.
class Document(models.Model):
    #aqui se crea los campos del modelo y dentro del los campos se especidica los datos
    title=models.CharField("Documento", max_length=60)
    description=models.CharField('Descripcion',max_length=120,null=True)
    document = models.FileField(upload_to='doc/')  # Se guardará en MEDIA_ROOT/documentos/
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'documento'
        verbose_name_plural = 'documentos'
        ordering=["title"]
       
        
    def __str__(self):  
        return str(self.title)+str(self.document)+str(self.date)