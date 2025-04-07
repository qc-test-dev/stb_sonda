from django.contrib import admin
from .models import Document
# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'document',
        'date',)
    
    search_fields=('title',)

admin.site.register(Document,DocumentAdmin)