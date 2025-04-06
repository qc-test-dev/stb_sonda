from django.shortcuts import render
from .models import Apk
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,CreateView,TemplateView)
from .forms import *
# Create your views here.
class ApkListView(LoginRequiredMixin,ListView):
    model = Apk
    context_object_name = 'apks'
    template_name='apks/listAllApks.html'
    paginate_by=15
    ordering='title'
    login_url = '/accounts/login/'

class ApkCreateView(LoginRequiredMixin,CreateView):
    model = Apk
    template_name = "apks/createApk.html"
    form_class = APKForm  # Usa el formulario personalizado
    
    def form_valid(self, form):
        document = form.save(commit=False)
        document.save()
        return super(ApkCreateView,self).form_valid(form)

    success_url = reverse_lazy('apk_app:allApks')
    login_url = '/accounts/login/'
class ListBySearchApksListView(ListView):
    model = Apk
    template_name = "apks/search.html"
    context_object_name='apks'
    def get_queryset(self):
        search = self.request.GET.get('search','')
        list= Apk.objects.filter(title__contains=search)
        print(list)
        return list