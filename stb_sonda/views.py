# Django views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import subprocess
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse,StreamingHttpResponse
import os, time,datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Datos de STBs (hardcodeados por ahora)
stbs = [
    {"name": "ZTE B866V2", "ip": "192.168.0.108"},
    {"name": "ZTE B866V2", "ip": "localhost"},
    {"name": "STB 1", "ip": "172.16.205.62"},
    {"name": "STB 2", "ip": "172.16.216.5"},
    {"name": "STB 3", "ip": "172.16.208.1"},
    {"name": "STB 4", "ip": "172.16.220.3"},
    {"name": "STB 5", "ip": "172.16.201.3"},
    {"name": "STB 6", "ip": "172.16.215.14"},
    {"name": "STB 7", "ip": "172.16.200.5"},
    {"name": "STB 7", "ip": "172.16.200.14"},
]


def check_device_connected(ip):
    """Solo verifica si el dispositivo está conectado sin intentar conexión"""
    result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, text=True)
    # Un dispositivo conectado aparecerá como "ip:5555 device" en la salida
    device_line = f"{ip}:5555"
    return "connected" if device_line in result.stdout else "disconnected"


def connect_device(ip):
    """Intenta conectar el dispositivo con un timeout de 1 segundo"""
    adb_port_tcpip = '5555'
    ip_port = f"{ip}:{adb_port_tcpip}"
    try:
        result = subprocess.run(
            ["adb", "connect", ip_port],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=1  # Timeout de 1 segundo
        )
        return "connected" if "connected to" in result.stdout else "timeout"
    except subprocess.TimeoutExpired:
        return "timeout"
    except Exception as e:
        print(f"Error connecting to {ip}: {str(e)}")
        return "error"


@login_required
def home(request):
    # Verificar solo el estado de conexión de cada STB
    for stb in stbs:
        stb["status"] = check_device_connected(stb["ip"])
    
    return render(request, "home.html", {"stbs": stbs, "localhost": "localhost"})

def connect_adb(request, ip):
    """Intenta conectar dispositivo y muestra mensajes según resultado"""
    result = connect_device(ip)
    
    if result == "connected":
        messages.success(request, f"Dispositivo {ip} conectado correctamente")
    elif result == "timeout":
        messages.error(request, f"Error: Tiempo de espera agotado al conectar con {ip}")
    else:
        messages.error(request, f"Error al conectar con el dispositivo {ip}")
    
    # Redireccionar a la página principal después de intentar conectar
    return redirect('home')


def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    return redirect("/home/")

# Redirect to login if not authenticated


def get_logs(request, ip):
    one_hour_ago = (datetime.datetime.now() - datetime.timedelta(hours=24)).strftime("%m-%d %H:%M:%S.%3m")
    print(one_hour_ago)
    try:
        # Comando ADB para obtener los logs
        log_file = f"{ip}_logs.txt"
        result = subprocess.run(
            ["adb", "-s", ip, "shell", "logcat", "-d","-T", f'"{one_hour_ago}"'],  # 1440 minutos = 24 horas
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)
        time.sleep(7)  # Esperar 1 segundo para que el archivo se cree
        if result:
            # Guardar logs en un archivo
            with open(log_file, "w") as f:
                f.write(result.stdout)
            # Leer el archivo y enviarlo como respuesta de descarga
            with open(log_file, "r") as f:
                response = HttpResponse(f.read(), content_type="text/plain")
                response["Content-Disposition"] = f"attachment; filename={log_file}"
            # Eliminar el archivo después de enviarlo
            os.remove(log_file)
            return response
        else:
            return HttpResponse("Error al obtener los logs", status=500)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
    
def get_logs_1h(request, ip):
    one_hour_ago = (datetime.datetime.now() - datetime.timedelta(minutes=30)).strftime("%m-%d %H:%M:%S.%3m")
    print(one_hour_ago)
    try:
        # Comando ADB para obtener los logs
        log_file = f"{ip}_logs.txt"
        result = subprocess.run(
            ["adb", "-s", ip, "shell", "logcat", "-d","-T", f'"{one_hour_ago}"'],  # 1440 minutos = 24 horas
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)
        time.sleep(7)  # Esperar 1 segundo para que el archivo se cree
        if result:
            # Guardar logs en un archivo
            with open(log_file, "w") as f:
                f.write(result.stdout)
            # Leer el archivo y enviarlo como respuesta de descarga
            with open(log_file, "r") as f:
                response = HttpResponse(f.read(), content_type="text/plain")
                response["Content-Disposition"] = f"attachment; filename={log_file}"
            # Eliminar el archivo después de enviarlo
            os.remove(log_file)
            return response
        else:
            return HttpResponse("Error al obtener los logs", status=500)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

# Instalar una APK desde la carpeta static
def install_apk(request, ip):
    try:
        apk_path = os.path.join("static", "app.apk")  # Ruta de la APK en static
        if not os.path.exists(apk_path):
            return HttpResponse("APK no encontrada en la carpeta static", status=404)
        # Comando ADB para instalar la APK
        result = subprocess.run(
            ["adb", "-s", ip, "install", apk_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            return HttpResponse("APK instalada exitosamente")
        else:
            return HttpResponse("Error al instalar la APK", status=500)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
    

def list_apks(request, ip):
    apk_folder = os.path.join("static")  # Carpeta donde se almacenan las APKs
    try:
        # Lista las APKs disponibles en la carpeta static
        apks = [f for f in os.listdir(apk_folder) if f.endswith(".apk")]
        return render(request, "list_apks.html", {"apks": apks, "ip": ip})
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)



def install_selected_apk(request, ip):
    if request.method == "POST":
        apk_name = request.POST.get("apk")
        apk_path = os.path.join("static", apk_name)

        if not os.path.exists(apk_path):
            return HttpResponse(f"APK '{apk_name}' no encontrada en la carpeta static", status=404)

        try:
            process = subprocess.run(
                ["adb", "-s", ip, "install", apk_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if process.returncode == 0:
                return HttpResponse("Instalación finalizada")
            else:
                return HttpResponse("Error en la instalación")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)
    else:
        return HttpResponse("Método no permitido", status=405)