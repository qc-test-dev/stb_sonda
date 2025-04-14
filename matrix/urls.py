from django.urls import path
from . import views

urlpatterns = [
    path('excel/', views.lista_archivos_excel, name='lista_excel'),
    path('excel/<str:nombre_archivo>/', views.mostrar_archivo_excel, name='mostrar_excel'),
]
