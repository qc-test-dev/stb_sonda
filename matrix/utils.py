import pandas as pd
import openpyxl
from .models import CasoDePrueba

def importar_matriz_desde_excel(matriz, ruta_excel):
    wb = openpyxl.load_workbook(ruta_excel)
    sheet = wb.active

    for fila in sheet.iter_rows(min_row=2, values_only=True):
        alcance = fila[0] if fila[0] else "Desconocido"
        fase = fila[1] if fila[1] else "Desconocido"
        caso_de_prueba = fila[2] if fila[2] else "Caso sin descripción"
        criticidad = fila[3] if fila[3] else "Bloqueante"
        nota = fila[4] if len(fila) > 4 and fila[4] else ""

        CasoDePrueba.objects.create(
            matriz=matriz,
            alcance=alcance,
            fase=fase,
            caso_de_prueba=caso_de_prueba,
            estado="por_ejecutar",
            criticidad=criticidad,
            nota=nota
        )

def copiar_casos_de_matriz_base(matriz_origen, matriz_destino):
    casos = matriz_origen.casos.all()
    for caso in casos:
        CasoDePrueba.objects.create(
            matriz=matriz_destino,
            alcance=caso.alcance,
            fase=caso.fase,
            caso_de_prueba=caso.caso_de_prueba,
            estado="por_ejecutar",
            criticidad=caso.criticidad,
            nota=caso.nota
        )
