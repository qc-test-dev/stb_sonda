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
    xls = pd.ExcelFile(ruta_archivo)
    hojas = xls.sheet_names

    if request.method == "POST":
        nombre_hoja_seleccionada = request.POST.get('hoja_seleccionada')
        df = pd.read_excel(xls, sheet_name=nombre_hoja_seleccionada)
        tabla_html = df.to_html(classes='table table-bordered', index=False, border=0)
        return render(request, 'excel_files/viewExcel.html', {
            'tablas': [{'nombre_hoja': nombre_hoja_seleccionada, 'tabla_html': tabla_html}],
            'nombre_actual': nombre_archivo,
            'hojas': hojas,
            'hoja_seleccionada': nombre_hoja_seleccionada
        })

    return render(request, 'excel_files/viewExcel.html', {
        'nombre_actual': nombre_archivo,
        'hojas': hojas
    })

# def mostrar_archivo_excel(request, nombre_archivo):
#     ruta_archivo = os.path.join(settings.EXCEL_DIR, nombre_archivo)
#     try:
#         xls = pd.ExcelFile(ruta_archivo)
#         hojas = []

#         for nombre_hoja in xls.sheet_names:
#             df = pd.read_excel(xls, sheet_name=nombre_hoja)
#             tabla_html = df.to_html(classes='table table-bordered', index=False, border=0)
#             hojas.append({
#                 'nombre_hoja': nombre_hoja,
#                 'tabla_html': tabla_html
#             })

#         return render(request, 'excel_files/showExcel.html', {
#             'nombre_archivo': nombre_archivo,
#             'hojas': hojas
#         })

#     except Exception as e:
#         return render(request, 'excel_files/showExcel.html', {
#             'nombre_archivo': nombre_archivo,
#             'error': str(e)
#         })

