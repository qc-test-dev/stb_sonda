from django.urls import path
from . import views
app_name='matrix_app'
urlpatterns = [
    path('', views.super_matriz_dashboard, name='dashboard_super_matrices'),
    path('supermatriz/<int:super_matriz_id>/', views.detalle_super_matriz, name='detalle_super_matriz'),
    path('supermatriz/<int:super_matriz_id>/', views.detalle_super_matriz, name='detalle_super_matriz'),
    path('matriz/<int:matriz_id>/', views.detalle_matriz, name='detalle_matriz'),  # Esta es la URL para detalle_matriz
]
