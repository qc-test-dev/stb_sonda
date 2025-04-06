from django.contrib import admin
from .models import Apk
# Register your models here.
class ApkAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'document',
        'date',)
    
    search_fields=('title',)

admin.site.register(Apk,ApkAdmin)