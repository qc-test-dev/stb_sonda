from django.contrib import admin
from .models import SuperMatriz, CasoDePrueba, Matriz

# Inline para mostrar las matrices dentro del admin de SuperMatriz
class MatrizInline(admin.TabularInline):
    model = Matriz
    extra = 1  # Cuántas filas en blanco se mostrarán por defecto

# Inline para mostrar los casos de prueba dentro del admin de Matriz
class CasoDePruebaInline(admin.TabularInline):
    model = CasoDePrueba
    extra = 1  # Cuántas filas en blanco se mostrarán por defecto

class SuperMatrizAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'fecha_creacion')
    inlines = [MatrizInline]  # Mostrar matrices relacionadas

class MatrizAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'super_matriz', 'fecha_creacion')
    inlines = [CasoDePruebaInline]  # Mostrar casos de prueba relacionados

admin.site.register(SuperMatriz, SuperMatrizAdmin)
admin.site.register(Matriz, MatrizAdmin)
admin.site.register(CasoDePrueba)
