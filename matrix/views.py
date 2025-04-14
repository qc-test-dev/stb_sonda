import os
from django.conf import settings
from django.shortcuts import render
import pandas as pd

def lista_archivos_excel(request):
    carpeta = settings.EXCEL_DIR
    archivos = [f for f in os.listdir(carpeta) if f.endswith('.xlsx') or f.endswith('.xls')]
    return render(request, 'excel_files/showExcel.html', {'archivos': archivos})

def mostrar_archivo_excel(request, nombre_archivo):
    ruta_archivo = os.path.join(settings.EXCEL_DIR, nombre_archivo)
    df = pd.read_excel(ruta_archivo)
    tabla_html = df.to_html(classes='table table-bordered', index=False, border=0)
    return render(request, 'excel_files/showExcel.html', {
        'tabla_html': tabla_html,
        'archivos': [f for f in os.listdir(settings.EXCEL_DIR) if f.endswith('.xlsx') or f.endswith('.xls')],
        'nombre_actual': nombre_archivo
    })
