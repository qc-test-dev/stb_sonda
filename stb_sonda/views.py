from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import subprocess
from django.http import JsonResponse, HttpResponse
import requests

@login_required
def home(request):
    # Obtener lista de dispositivos ADB conectados dinámicamente
    devices = []
    try:
        result = subprocess.run(["adb", "devices"], check=True, text=True, capture_output=True)
        lines = result.stdout.splitlines()[1:]  # Ignorar el encabezado
        devices = [{"ip": line.split("\t")[0], "name": "Dispositivo"} for line in lines if "\tdevice" in line]
    except subprocess.CalledProcessError as e:
        print(f"Error obteniendo dispositivos ADB: {e.stderr}")

    return render(request, 'home.html', {"devices": devices})


@login_required
def connect_device(request, ip):
    # Renderizar la página de conexión del dispositivo
    return render(request, 'connect.html', {'ip': ip})


def live_view(request, ip):
    # URL del servidor ws-scrcpy
    ws_scrcpy_url = f"http://10.42.0.1:8000/"
    return render(request, 'live.html', {'ip': ip, 'ws_scrcpy_url': ws_scrcpy_url})


def proxy_to_ws_scrcpy(request, ip_port):
    # Proxy para redirigir al servidor ws-scrcpy
    ws_scrcpy_url = f"http://{ip_port}{request.path.replace('/stream', '')}"
    try:
        response = requests.request(
            method=request.method,
            url=ws_scrcpy_url,
            headers={key: value for key, value in request.headers.items() if key.lower() != 'host'},
            params=request.GET,
            data=request.body,
            stream=True,
        )
        django_response = HttpResponse(
            content=response.content,
            status=response.status_code,
        )
        for header, value in response.headers.items():
            if header.lower() not in ['content-encoding', 'transfer-encoding', 'connection']:
                django_response[header] = value
        return django_response
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
