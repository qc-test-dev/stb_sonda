# Django views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import subprocess
from django.contrib.auth.views import LoginView, LogoutView

# Datos de STBs (hardcodeados por ahora)
stbs = [
    {"name": "ZTE B866V2", "ip": "10.42.0.50", "status": "1"},
    {"name": "ZTE B866V2", "ip": "localhost", "status": "1"},
    # Agrega más STBs según sea necesario
]

def check_adb_connection(ip):
    try:
        result = subprocess.run(
            ["adb", "connect", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return "connected" if "connected to" in result.stdout.decode() else "disconnected"
    except Exception as e:
        return "disconnected"

@login_required
def home(request):
    for stb in stbs:
        stb["status"] = check_adb_connection(stb["ip"])
    return render(request, "home.html", {"stbs": stbs})


def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    return redirect("/home/")
# Redirect to login if not authenticated
