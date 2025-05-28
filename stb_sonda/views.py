# Django views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from matrix.models import SuperMatriz
from matrix.forms import SuperMatrizForm
from matrix.utils import importar_validates_desde_excel
import os
@login_required
def home(request):
    # Obtener estado de conexión de los STB (si tienes lógica, añádela aquí)
    # Por ejemplo: stb_status = check_stb_connections()

    # SuperMatrices
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

    return render(request, "home.html", {
        # 'stb_status': stb_status,  # descomenta si tienes algo para pasar
        'form': form,
        'super_matrices': super_matrices,
    })
def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    return redirect("/home/")

# Redirect to login if not authenticated