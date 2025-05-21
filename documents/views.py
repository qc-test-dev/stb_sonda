from django.shortcuts import render
from .models import Document
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,CreateView,TemplateView)
from .forms import DocumentForm

# Create your views here.


import os
from django.conf import settings
from django.views.generic import TemplateView


# class listAllDocumentListView(LoginRequiredMixin,ListView):
#     model = Document
#     context_object_name = 'docs'
#     template_name='documents/listAllDocuments.html'
#     paginate_by=10
#     ordering='title'
#     login_url = '/accounts/login/'
# class successView(TemplateView):
#     template_name = "documents/success.html"

class listAllDocumentListView(LoginRequiredMixin, ListView):
    model = Document
    context_object_name = 'docs'
    template_name = 'documents/listAllDocuments.html'
    paginate_by = 10
    ordering = 'title'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Carpeta static/docs
        docs_path = os.path.join(settings.BASE_DIR, 'static/docs')
        if os.path.exists(docs_path):
            archivos = os.listdir(docs_path)
            archivos = [f'docs/{a}' for a in archivos if not a.startswith('.')]
        else:
            archivos = []
        context['archivos'] = archivos
        return context

# class DocumentCreateView(LoginRequiredMixin,CreateView):
#     model = Document
#     template_name = "documents/createDoc.html"
#     form_class = DocumentForm  # Usa el formulario personalizado
    
#     def form_valid(self, form):
#         document = form.save(commit=False)
#         document.save()
#         return super(DocumentCreateView,self).form_valid(form)

#     success_url = reverse_lazy('doc_app:allDoc')  # Redirección después de crear
#     login_url = '/accounts/login/'
# class ListBySearchDocumentsListView(ListView):
#     model = Document
#     template_name = "documents/search.html"
#     context_object_name='docs'
#     def get_queryset(self):
#         search = self.request.GET.get('search','')
#         list= Document.objects.filter(title__contains=search)
#         return list
class ListBySearchDocumentsListView(ListView):
    model = Document
    template_name = "documents/search.html"
    context_object_name = 'docs'

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return Document.objects.filter(title__icontains=search)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        static_docs_dir = os.path.join(settings.BASE_DIR, 'static/docs')
        archivos_encontrados = []

        if os.path.exists(static_docs_dir):
            for root, dirs, files in os.walk(static_docs_dir):
                for file in files:
                    if search.lower() in file.lower():
                        # Crea la ruta relativa para usar con {% static %}
                        relative_path = os.path.relpath(os.path.join(root, file), os.path.join(settings.BASE_DIR, 'static'))
                        archivos_encontrados.append(relative_path.replace("\\", "/"))  # para Windows

        context['archivos'] = archivos_encontrados
        return context
