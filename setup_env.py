import os
import subprocess
import sys

venv_dir = "venv"
requirements_file = "requirements.txt"

if not os.path.isfile(requirements_file):
    print(f" No se encontró el archivo '{requirements_file}'.")
    sys.exit(1)

if not os.path.exists(venv_dir):
    print(" Creando entorno virtual...")
    subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
else:
    print(" El entorno virtual ya existe.")

# Detecta correctamente la ruta del pip (pip.exe en Windows)
pip_executable = "pip.exe" if os.name == "nt" else "pip"
pip_path = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", pip_executable)

if not os.path.exists(pip_path):
    print(f" pip no se encontró en '{pip_path}'.")
    print(" Solución: Asegúrate de que el entorno virtual esté bien creado.")
    print(" Puedes intentar recrearlo con: python -m venv venv --upgrade-deps")
    sys.exit(1)

print(" Instalando dependencias desde requirements.txt...")
subprocess.check_call([pip_path, "install", "-r", requirements_file])

print("\n Entorno virtual preparado.")
print(f" Para activarlo:\n{'venv\\Scripts\\activate' if os.name == 'nt' else 'source venv/bin/activate'}")
