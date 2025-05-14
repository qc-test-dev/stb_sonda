from django.shortcuts import render, redirect, get_object_or_404
from .forms import SuperMatrizForm, MatrizForm, CasoDePruebaForm,ValidateForm,ValidateEstadoForm,DetallesValidateForm
from .models import SuperMatriz, Matriz,Validate
from .utils import importar_matriz_desde_excel, copiar_casos_de_matriz_base,importar_validates_desde_excel
import os

def super_matriz_dashboard(request):
    super_matrices = SuperMatriz.objects.all()

    if request.method == 'POST':
        form = SuperMatrizForm(request.POST)
        if form.is_valid():
            # Crear la SuperMatriz
            super_matriz = form.save()

            # Crear matriz base asociada
            matriz_base = Matriz.objects.create(
                super_matriz=super_matriz,
                nombre="Matriz Base"
            )

            # Importar casos de prueba
            ruta_excel_matriz = os.path.join('static', 'excel_files', 'matriz_base.xlsx')
            importar_matriz_desde_excel(matriz_base, ruta_excel_matriz)

            # Importar validates
            ruta_excel_validates = os.path.join('static', 'excel_files', 'validates.xlsx')
            importar_validates_desde_excel(super_matriz, ruta_excel_validates)

            return redirect('matrix_app:detalles_validate_modal', super_matriz_id=super_matriz.id)
    else:
        form = SuperMatrizForm()

    return render(request, 'excel_files/super_matriz_dashboard.html', {
        'form': form,
        'super_matrices': super_matrices
    })
def detalle_super_matriz(request, super_matriz_id):
    super_matriz = get_object_or_404(SuperMatriz, id=super_matriz_id)
    matrices = super_matriz.matrices.all()
    validates = super_matriz.validates.all()
    tickets = super_matriz.tickets_por_levantar.all()

    if request.method == 'POST':
        if 'crear_matriz' in request.POST:
            form = MatrizForm(request.POST)
            if form.is_valid():
                nueva_matriz = form.save(commit=False)
                nueva_matriz.super_matriz = super_matriz
                nueva_matriz.save()

                matriz_base = super_matriz.matrices.first()
                if matriz_base:
                    copiar_casos_de_matriz_base(matriz_base, nueva_matriz)

                return redirect('matrix_app:detalle_super_matriz', super_matriz_id=super_matriz.id)

        elif 'crear_validate' in request.POST:
            validate_form = ValidateForm(request.POST)
            if validate_form.is_valid():
                validate = validate_form.save(commit=False)
                validate.super_matriz = super_matriz
                validate.save()
                return redirect('matrix_app:detalle_super_matriz', super_matriz_id=super_matriz.id)

        elif 'crear_ticket' in request.POST:
            ticket_form = TicketPorLevantarForm(request.POST)
            if ticket_form.is_valid():
                ticket = ticket_form.save(commit=False)
                ticket.super_matriz = super_matriz
                ticket.save()
                return redirect('matrix_app:detalle_super_matriz', super_matriz_id=super_matriz.id)

    else:
        form = MatrizForm()
        validate_form = ValidateForm()

    return render(request, 'excel_files/detalle_super_matriz.html', {
        'super_matriz': super_matriz,
        'form': form,
        'matrices': matrices,
        'validate_form': validate_form,
        'ticket_form': ticket_form,
        'validates': validates,
        'tickets': tickets,
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
def editar_validates(request, super_matriz_id):
    super_matriz = get_object_or_404(SuperMatriz, id=super_matriz_id)
    validates = Validate.objects.filter(super_matriz=super_matriz)

    formularios = []

    if request.method == 'POST':
        for validate in validates:
            form = ValidateEstadoForm(request.POST, prefix=str(validate.id), instance=validate)
            if form.is_valid():
                form.save()
        return redirect('matrix_app:editar_validates', super_matriz_id=super_matriz.id)
    else:
        for validate in validates:
            form = ValidateEstadoForm(prefix=str(validate.id), instance=validate)
            formularios.append((validate, form))

    return render(request, 'excel_files/editar_validates.html', {
        'super_matriz': super_matriz,
        'formularios_validates': formularios
    })
def detalles_validate_modal(request, super_matriz_id):
    super_matriz = SuperMatriz.objects.get(id=super_matriz_id)

    if request.method == 'POST':
        form = DetallesValidateForm(request.POST)
        if form.is_valid():
            detalles = form.save(commit=False)
            detalles.super_matriz = super_matriz
            detalles.save()
            return redirect('matrix_app:detalle_super_matriz', super_matriz_id=super_matriz.id)
    else:
        form = DetallesValidateForm()

    return render(request, 'excel_files/detalles_validate_modal.html', {
        'form': form,
        'super_matriz': super_matriz
    })
