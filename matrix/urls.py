from django.urls import path
from . import views
app_name='matrix_app'
#matrix_app:dashboard_super_matrices
urlpatterns = [
    path('supermatriz/<int:super_matriz_id>/', views.detalle_super_matriz, name='detalle_super_matriz'),
    path('matriz/<int:matriz_id>/', views.detalle_matriz, name='detalle_matriz'),
    path('editar_validates/<int:super_matriz_id>/', views.editar_validates, name='editar_validates'),
    path('detalles_validate_modal/<int:super_matriz_id>/', views.detalles_validate_modal, name='detalles_validate_modal'),# Esta es la URL para detalle_matriz
    path('super_matriz/<int:super_matriz_id>/tickets/', views.tickets_por_levantar_view, name='tickets_por_levantar'),
    path('editar_ticket/<int:ticket_id>/', views.editar_ticket, name='editar_ticket'),
    
]   


