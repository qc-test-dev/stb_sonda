from django.conf import settings
from django.shortcuts import render
from .models import Apk
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,CreateView,TemplateView)
from .forms import *
import os 
# Create your views here.
class ApkListView(LoginRequiredMixin, ListView):
    model = Apk
    context_object_name = 'apks'
    template_name = 'apks/listAllApks.html'
    paginate_by = 15
    ordering = 'title'
    login_url = '/accounts/login/'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Buscar archivos en static/apks
        apks_path = os.path.join(settings.BASE_DIR, 'static', 'apks')
        archivos = []

        if os.path.exists(apks_path):
            for nombre_archivo in os.listdir(apks_path):
                archivos.append(f"apks/{nombre_archivo}")

        context['archivos'] = archivos
        return context
# class ApkCreateView(LoginRequiredMixin,CreateView):
#     model = Apk
#     template_name = "apks/createApk.html"
#     form_class = APKForm  # Usa el formulario personalizado
    
#     def form_valid(self, form):
#         document = form.save(commit=False)
#         document.save()
#         return super(ApkCreateView,self).form_valid(form)

    # success_url = reverse_lazy('apk_app:allApks')
    # login_url = '/accounts/login/'
class ListBySearchApksListView(ListView):
    model = Apk
    template_name = "apks/search.html"
    context_object_name = 'apks'

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return Apk.objects.filter(title__icontains=search)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '').lower()

        # Buscar archivos en static/apks
        apks_path = os.path.join(settings.BASE_DIR, 'static', 'apks')
        archivos = []

        if os.path.exists(apks_path):
            for nombre_archivo in os.listdir(apks_path):
                if search in nombre_archivo.lower():
                    archivos.append(f"apks/{nombre_archivo}")

        context['archivos'] = archivos
        return context