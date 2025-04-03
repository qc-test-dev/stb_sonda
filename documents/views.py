from django.shortcuts import render
from .models import Document
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,CreateView,TemplateView)
from .forms import DocumentForm

# Create your views here.

class listAllDocumentListView(LoginRequiredMixin,ListView):
    model = Document
    context_object_name = 'docs'
    template_name='documents/listAllDocuments.html'
    paginate_by=10
    ordering='title'
    login_url = '/accounts/login/'
class successView(TemplateView):
    template_name = "documents/success.html"

class DocumentCreateView(LoginRequiredMixin,CreateView):
    model = Document
    template_name = "documents/createDoc.html"
    form_class = DocumentForm  # Usa el formulario personalizado
    
    def form_valid(self, form):
        document = form.save(commit=False)
        document.save()
        return super(DocumentCreateView,self).form_valid(form)

    success_url = reverse_lazy('doc_app:allDoc')  # Redirección después de crear
    login_url = '/accounts/login/'
class ListBySearchDocumentsListView(ListView):
    model = Document
    template_name = "documents/search.html"
    context_object_name='docs'
    def get_queryset(self):
        print('++++++++++++++++++++++++++++')
        search = self.request.GET.get('search','')
        print(f'{search}')
        list= Document.objects.filter(title__contains=search)
        print(list)
        return list

