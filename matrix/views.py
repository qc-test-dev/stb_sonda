import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import random
from stb_sonda import settings
from .forms import (
    SuperMatrizForm, MatrizForm, CasoDePruebaForm,
    ValidateForm, ValidateEstadoForm, DetallesValidateForm,
    TicketPorLevantarForm
)
from .models import SuperMatriz, Matriz, Validate,TicketPorLevantar
from .utils import importar_validates_desde_excel,importar_matriz_desde_excel
from django.urls import reverse

def super_matriz_dashboard(request):
    super_matrices = SuperMatriz.objects.all()

    if request.method == 'POST':
        form = SuperMatrizForm(request.POST)
        if form.is_valid():
            super_matriz = form.save()

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

    matrices_info = []
    for matriz in matrices:
        casos = matriz.casos.all()
        total_casos = casos.count()
        estados_interes = ['funciona', 'falla_nueva', 'falla_persistente']
        casos_filtrados = casos.filter(estado__in=estados_interes).count()

        porcentaje = (casos_filtrados / total_casos * 100) if total_casos > 0 else 0

        matrices_info.append({
            'matriz': matriz,
            'total_casos': total_casos,
            'casos_filtrados': casos_filtrados,
            'porcentaje': round(porcentaje, 2),
        })

    # Inicializar formularios por defecto
    form = MatrizForm()
    validate_form = ValidateForm()

    if request.method == 'POST':
        # Crear Matriz
        if 'crear_matriz' in request.POST:
            form = MatrizForm(request.POST)
            if form.is_valid():
                nueva_matriz = form.save(commit=False)
                nueva_matriz.super_matriz = super_matriz

                alcance_seleccionado = request.POST.get('alcance', '')
                valores_a_incluir = set(alcance_seleccionado.split(',')) if alcance_seleccionado else set()

                nueva_matriz.alcances_utilizados = ",".join(sorted(valores_a_incluir))
                nueva_matriz.save()

                ruta_excel_matriz = os.path.join('static', 'excel_files', 'matriz_base.xlsx')
                importar_matriz_desde_excel(nueva_matriz, ruta_excel_matriz, valores_a_incluir)

                testers_seleccionados = form.cleaned_data.get('testers', [])
                regiones_seleccionados = form.cleaned_data.get('regiones', [])
                casos = list(nueva_matriz.casos.all())
                random.shuffle(regiones_seleccionados)
                random.shuffle(testers_seleccionados)
                random.shuffle(casos)
                for idx, caso in enumerate(casos):
                    caso.tester = testers_seleccionados[idx % len(testers_seleccionados)] if testers_seleccionados else ''
                    caso.tester+='-'+regiones_seleccionados[idx % len(regiones_seleccionados)] if regiones_seleccionados else ''
                    caso.save()

                return redirect('matrix_app:detalle_super_matriz', super_matriz_id=super_matriz.id)

        # Crear Validate
        elif 'crear_validate' in request.POST:
            validate_form = ValidateForm(request.POST)
            if validate_form.is_valid():
                validate = validate_form.save(commit=False)
                validate.super_matriz = super_matriz
                validate.save()
                return redirect('matrix_app:detalle_super_matriz', super_matriz_id=super_matriz.id)

    return render(request, 'excel_files/detalle_super_matriz.html', {
        'super_matriz': super_matriz,
        'matrices_info': matrices_info,
        'form': form,
        'validate_form': validate_form,
        'validates': validates,
    })


def detalle_matriz(request, matriz_id):
    matriz = get_object_or_404(Matriz, id=matriz_id)
    casos_de_prueba = matriz.casos.all()
    super_matriz_id = matriz.super_matriz.id

    # Obtener lista de filtros si existen
    alcances_lista = []
    if matriz.alcances_utilizados:
        alcances_lista = matriz.alcances_utilizados.split(',')

    # Obtener lista única de testers desde los casos
    testers_disponibles = casos_de_prueba.values_list('tester', flat=True).distinct()

    # Filtrar por tester si viene en la URL (GET)
    tester_filtrado = request.GET.get('tester')
    if tester_filtrado:
        casos_de_prueba = casos_de_prueba.filter(tester=tester_filtrado)

    if request.method == 'POST':
        success = True
        for caso in casos_de_prueba:
            form = CasoDePruebaForm(request.POST, instance=caso, prefix=f"caso_{caso.id}")
            if form.is_valid():
                form.save()
            else:
                success = False

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if success:
                return JsonResponse({'status': 'ok'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Formulario inválido'}, status=400)
        else:
            return redirect('matrix_app:detalle_matriz', matriz_id=matriz.id)

    formularios_casos_de_prueba = [
        (caso, CasoDePruebaForm(instance=caso, prefix=f"caso_{caso.id}"))
        for caso in casos_de_prueba
    ]

    return render(request, 'excel_files/detalle_matriz.html', {
        'matriz': matriz,
        'formularios_casos_de_prueba': formularios_casos_de_prueba,
        'super_matriz_id': super_matriz_id,
        'alcances_lista': alcances_lista,
        'testers_disponibles': testers_disponibles,
        'tester_filtrado': tester_filtrado,  # por si quieres marcar cuál está activo
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
    super_matriz = get_object_or_404(SuperMatriz, id=super_matriz_id)

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

def tickets_por_levantar_view(request, super_matriz_id):
    super_matriz = get_object_or_404(SuperMatriz, id=super_matriz_id)
    tickets = TicketPorLevantar.objects.filter(super_matriz=super_matriz)

    if request.method == 'POST':
        form = TicketPorLevantarForm(request.POST)
        if form.is_valid():
            nuevo_ticket = form.save(commit=False)
            nuevo_ticket.super_matriz = super_matriz
            nuevo_ticket.save()
            return redirect('matrix_app:tickets_por_levantar', super_matriz_id=super_matriz.id)
    else:
        form = TicketPorLevantarForm()

    return render(request, 'excel_files/tickets_por_levantar.html', {
        'super_matriz': super_matriz,
        'tickets': tickets,
        'form': form,
    })

def editar_ticket(request, ticket_id):
    ticket = get_object_or_404(TicketPorLevantar, id=ticket_id)

    if request.method == 'POST':
        ticket.ticket_SCT = request.POST.get('ticket_SCT', '').strip()
        ticket.BRF = request.POST.get('BRF', '').strip()
        ticket.desc = request.POST.get('desc', '').strip()
        ticket.nota = request.POST.get('nota', '').strip()
        ticket.url = request.POST.get('url', '').strip()
        ticket.save()
        
        # Redirige a la página de lista de tickets de la supermatriz
        return redirect(reverse('matrix_app:detalle_tickets', args=[ticket.super_matriz.id]))

