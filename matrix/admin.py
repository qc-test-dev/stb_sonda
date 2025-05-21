from django.contrib import admin
from .models import SuperMatriz, CasoDePrueba, Matriz,Validate,DetallesValidate


class MatrizInline(admin.TabularInline):
    model = Matriz
    extra = 1  

class CasoDePruebaInline(admin.TabularInline):
    model = CasoDePrueba
    extra = 1  
class SuperMatrizAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'fecha_creacion')
    inlines = [MatrizInline]  

class MatrizAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'super_matriz', 'fecha_creacion')
    inlines = [CasoDePruebaInline] 

admin.site.register(SuperMatriz, SuperMatrizAdmin)
admin.site.register(Matriz, MatrizAdmin)
admin.site.register(CasoDePrueba)
admin.site.register(Validate)
admin.site.register(DetallesValidate)