from django.urls import path
from .views import CustomLoginView, CustomLogoutView, manage_users

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('manage-users/', manage_users, name='manage_users'),
]

