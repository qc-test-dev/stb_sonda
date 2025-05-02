from django.shortcuts import render, redirect, get_object_or_404
from .forms import SuperMatrizForm, MatrizForm, CasoDePruebaForm
from .models import SuperMatriz, Matriz, CasoDePrueba
from .utils import importar_matriz_desde_excel, copiar_casos_de_matriz_base
import os

def super_matriz_dashboard(request):
    super_matrices = SuperMatriz.objects.all()

    if request.method == 'POST':
        form = SuperMatrizForm(request.POST)
        if form.is_valid():
            # Crear la SuperMatriz
            super_matriz = form.save()

            # Crear una matriz base asociada a esta super matriz
            matriz_base = Matriz.objects.create(
                super_matriz=super_matriz,
                nombre="Matriz Base"
            )

            # Cargar casos de prueba en esa matriz base desde Excel
            ruta_excel = os.path.join('static', 'excel_files', 'matriz_base.xlsx')
            importar_matriz_desde_excel(matriz_base, ruta_excel)

            return redirect('matrix_app:detalle_super_matriz', super_matriz_id=super_matriz.id)
    else:
        form = SuperMatrizForm()

    return render(request, 'excel_files/super_matriz_dashboard.html', {
        'form': form,
        'super_matrices': super_matrices
    })

def detalle_super_matriz(request, super_matriz_id):
    super_matriz = get_object_or_404(SuperMatriz, id=super_matriz_id)
    matrices = super_matriz.matrices.all()

    if request.method == 'POST':
        form = MatrizForm(request.POST)
        if form.is_valid():
            nueva_matriz = form.save(commit=False)
            nueva_matriz.super_matriz = super_matriz
            nueva_matriz.save()

            # Usamos la matriz base como fuente para copiar casos
            matriz_base = super_matriz.matrices.first()
            if matriz_base:
                copiar_casos_de_matriz_base(matriz_base, nueva_matriz)

            return redirect('matrix_app:detalle_super_matriz', super_matriz_id=super_matriz.id)
    else:
        form = MatrizForm()

    return render(request, 'excel_files/detalle_super_matriz.html', {
        'super_matriz': super_matriz,
        'form': form,
        'matrices': matrices,
    })

def detalle_matriz(request, matriz_id):
    matriz = get_object_or_404(Matriz, id=matriz_id)
    casos_de_prueba = matriz.casos.all()
    super_matriz_id = matriz.super_matriz.id

    if request.method == 'POST':
        for caso in casos_de_prueba:
            form = CasoDePruebaForm(request.POST, instance=caso, prefix=f"caso_{caso.id}")
            if form.is_valid():
                form.save()

        return redirect('matrix_app:detalle_matriz', matriz_id=matriz.id)

    formularios_casos_de_prueba = [
        (caso, CasoDePruebaForm(instance=caso, prefix=f"caso_{caso.id}"))
        for caso in casos_de_prueba
    ]

    return render(request, 'excel_files/detalle_matriz.html', {
        'matriz': matriz,
        'formularios_casos_de_prueba': formularios_casos_de_prueba,
        'super_matriz_id': super_matriz_id
    })
