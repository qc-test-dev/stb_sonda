import openpyxl
from .models import CasoDePrueba,Validate
import pandas as pd
def limpiar(valor):
    if isinstance(valor, str):
        return valor.strip()
    return valor

import openpyxl
from .models import CasoDePrueba

import openpyxl
from .models import CasoDePrueba

def importar_matriz_desde_excel(matriz, ruta_excel, alcances_permitidos=None):
    """
    Importa casos de prueba desde un archivo Excel y los asigna a una matriz.
    Filtra por alcance si se proporciona una lista de alcances_permitidos (['A', 'B', 'C']).
    Las filas incompletas (sin alcance, fase, caso o criticidad) se ignoran.
    """
    wb = openpyxl.load_workbook(ruta_excel)
    sheet = wb.active

    for fila in sheet.iter_rows(min_row=2, values_only=True):
        alcance = fila[0]
        fase = fila[1]
        caso_de_prueba = fila[2]
        criticidad = fila[4]
        nota = fila[5] if len(fila) > 5 else ""

        # Validar que los campos clave no estén vacíos
        if not (alcance and fase and caso_de_prueba and criticidad):
            continue  # Ignorar la fila si falta alguno

        # Filtrar por alcance si se especifica
        if alcances_permitidos and alcance not in alcances_permitidos:
            continue

        # Crear el caso de prueba
        CasoDePrueba.objects.create(
            matriz=matriz,
            alcance=alcance,
            fase=fase,
            caso_de_prueba=caso_de_prueba,
            estado="por_ejecutar",
            criticidad=criticidad,
            nota=nota or ""
        )


def importar_validates_desde_excel(super_matriz, ruta_excel):
    """
    Importa registros de 'Validate' desde un archivo Excel y los asigna a una SuperMatriz.
    Las filas incompletas (sin tester, ticket, descripcion, prioridad o estado) se ignoran.
    """
    wb = openpyxl.load_workbook(ruta_excel)
    sheet = wb.active

    empty_rows = 0

    for fila in sheet.iter_rows(min_row=2, values_only=True):
        if all(cell is None for cell in fila):
            empty_rows += 1
            if empty_rows > 5:
                break
            #print("Fila ignorada por estar incompleta")
            continue
        empty_rows = 0  # Reset counter si hay datos

        tester = fila[0]
        ticket = fila[1]
        descripcion = fila[2]
        prioridad = fila[3]
        estado = fila[4]

        # Ignorar si falta alguno de los campos obligatorios
        if not tester or not ticket or not descripcion or not prioridad or not estado:
            #print("Fila ignorada por campos vacíos obligatorios")
            continue

        Validate.objects.create(
            super_matriz=super_matriz,
            tester=tester,
            ticket=ticket,
            descripcion=descripcion,
            prioridad=prioridad,
            estado=estado
        )