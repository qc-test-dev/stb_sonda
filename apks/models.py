from django.db import models

# Create your models here.
class Apk(models.Model):
    #aqui se crea los campos del modelo y dentro del los campos se especidica los datos
    title=models.CharField("APK", max_length=15)
    document = models.FileField(upload_to='apk/')  # Se guardará en MEDIA_ROOT/documentos/
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'apk'
        verbose_name_plural = 'apks'
        ordering=["title"]
       
        
    def __str__(self):  
        return str(self.title)+str(self.document)+str(self.date)