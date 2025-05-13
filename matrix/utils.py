import openpyxl
from .models import CasoDePrueba

def limpiar(valor):
    if isinstance(valor, str):
        return valor.strip()
    return valor

import openpyxl
from .models import CasoDePrueba

def importar_matriz_desde_excel(matriz, ruta_excel):
    """
    Importa casos de prueba desde un archivo Excel y los asigna a una matriz.
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

        # Crear el caso de prueba
        CasoDePrueba.objects.create(
            matriz=matriz,
            alcance=alcance,
            fase=fase,
            caso_de_prueba=caso_de_prueba,
            estado="por_ejecutar",
            criticidad=criticidad,
            nota=nota or ""  # Vacío si es None
        )

def copiar_casos_de_matriz_base(matriz_origen, matriz_destino):
    """
    Copia todos los casos de prueba de una matriz base a otra matriz nueva.
    """
    casos = matriz_origen.casos.all()
    for caso in casos:
        CasoDePrueba.objects.create(
            matriz=matriz_destino,
            alcance=caso.alcance,
            fase=caso.fase,
            caso_de_prueba=caso.caso_de_prueba,
            estado="por_ejecutar",
            criticidad=caso.criticidad,
            nota=caso.nota or ""  # Asegura que no sea None
        )
