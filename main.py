import tkinter as tk
from tkinter import filedialog, ttk
import json
import os
import subprocess
import sys

def mostrar_mensaje(texto):
    salida_texto.insert(tk.END, texto + "\n")
    salida_texto.see(tk.END)  # Scroll automático al final

def examinar_ruta():
    ruta = filedialog.askdirectory()
    entrada_ruta.delete(0, tk.END)
    entrada_ruta.insert(0, ruta)

def guardar_json():
    datos = {
        "path": entrada_ruta.get(),
        "version": combo_version.get()
    }

    try:
        with open("MBconfig.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4)
        mostrar_mensaje("✅ Datos guardados en MBconfig.json")
    except Exception as e:
        mostrar_mensaje(f"❌ Error al guardar JSON: {e}")
 
    if getattr(sys, 'frozen', False):
        # Si está ejecutándose desde un exe generado por PyInstaller
        ruta_actual = os.path.dirname(sys.executable)
    else:
        # Si se ejecuta como script python normal
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
    
    # Crear carpeta Build
    carpeta_build = os.path.join(ruta_actual, "Build")
    try:
        os.makedirs(carpeta_build, exist_ok=True)
        mostrar_mensaje(f"📁 Carpeta 'Build' creada en: {carpeta_build}")
    except Exception as e:
        mostrar_mensaje(f"❌ Error al crear carpeta Build: {e}")

    # Ejecutar cmake ..
    try:
        resultado = subprocess.run(
            ["cmake", ".."],
            cwd=carpeta_build,
            capture_output=True,
            text=True
        )
        mostrar_mensaje("🛠️ CMake executed:")
        mostrar_mensaje(resultado.stdout)
        if resultado.stderr:
            mostrar_mensaje("⚠️ CMake errors:")
            mostrar_mensaje(resultado.stderr)
    except Exception as e:
        mostrar_mensaje(f"❌ Error during cmake execution: {e}")

# Interfaz
ventana = tk.Tk()
ventana.title("PT VS files generator")
ventana.geometry("500x300")
ventana.resizable(False, False)
ventana.configure( padx=10, pady=10)

infoFrame = tk.Frame(ventana)
infoFrame.pack(fill="x")

separator = tk.Frame(ventana, height=1, bd=0, bg="gray")
separator.pack(fill="x", pady=5)

verFrame = tk.Frame(ventana)
verFrame.pack(fill="x")

pathFrame = tk.Frame(ventana)
pathFrame.pack(fill="x")

# Información
tk.Label(infoFrame, text="Information:", 
         font=("Arial", 10, "bold"),
         wraplength=480, 
         justify="left", 
         ).pack(side="top")
tk.Label(infoFrame, text="This program generates Visual Studio project files in the Build folder to compile Palette Tools plugins for Autodesk MotionBuilder 2024 and earlier.", 
         font=("Arial", 9),
         wraplength=490, 
         justify="left", 
         ).pack(side="left")


# Selector versión
tk.Label(verFrame, 
         text="Versión:",
         font=("Arial", 10, "bold")
         ).pack(side="left")
combo_version = ttk.Combobox(verFrame, values=["2024", "2025", "2026"], state="readonly")
combo_version.set("2024")  # Valor por defecto
combo_version['width'] = 10
combo_version.pack(side="left")

# Carpeta MotionBuilder
tk.Label(pathFrame,
         text="MotionBuilder Path:",
         font=("Arial", 10, "bold")
         ).pack(side="left")
entrada_ruta = tk.Entry(pathFrame, width=35)
entrada_ruta.pack(side="left", padx=5)
tk.Button(pathFrame, text="Select Directory", command=examinar_ruta, width=15).pack(side="left")

# Área de salida
salida_texto = tk.Text(ventana, height=10, width=60, bg="#f0f0f0")
salida_texto.pack(fill="both", expand=True, padx=5, pady=5 )
scrollY = tk.Scrollbar(salida_texto, command=salida_texto.yview)
scrollY.pack(side="right", fill="y")
salida_texto.config(yscrollcommand=scrollY.set)

# Botón guardar
tk.Button(ventana, text="Generate", command=guardar_json).pack()


ventana.mainloop()