from django.urls import path
from . import views
app_name='matrix_app'
urlpatterns = [
    path('excel/', views.lista_archivos_excel, name='listExcel'),
    path('excel/<str:nombre_archivo>/', views.mostrar_archivo_excel, name='showExcel'),
]

