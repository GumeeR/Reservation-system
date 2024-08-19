import flet as ft
import os
from pathlib import Path
import pandas as pd
import io

documentos_path = Path.home() / 'Documents'

if not documentos_path.exists():
    documentos_path = Path.home() / 'Documentos'

historial_path = documentos_path / "Historial de reservas"
archivo_reservas = 'assets/reservas.xlsx'
archivo_destino = historial_path / 'reservas.xlsx'

def crear_carpeta_si_no_existe(path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"Carpeta creada: {path}")

def guardar_archivo_en_carpeta(contenido, ruta_destino):
    with open(ruta_destino, "wb") as archivo:
        archivo.write(contenido)
        print(f"Archivo guardado: {ruta_destino}")

def generar_archivo_reservas():
    if not Path(archivo_reservas).exists():
        print(f"Archivo de reservas no encontrado en {archivo_reservas}")
        return None

    try:
        df_reservas = pd.read_excel(archivo_reservas)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_reservas.to_excel(writer, index=False)
        return output.getvalue()
    except Exception as e:
        print(f"Error al leer el archivo de reservas: {e}")
        return None

def abrir_archivo(path):
    if os.name == 'nt':
        os.startfile(path)
    elif os.name == 'posix':
        subprocess.call(['open', path])

def mostrar_admin(page: ft.Page):
    def descargar_reservas(e):
        crear_carpeta_si_no_existe(historial_path)

        contenido = generar_archivo_reservas()
        
        if contenido:
            guardar_archivo_en_carpeta(contenido, archivo_destino)
            page.add(ft.Text("Archivo de reservas guardado exitosamente en 'Historial de reservas'."))
        else:
            page.add(ft.Text("Error al generar el archivo de reservas."))
        
        page.update()

    def abrir_informe(e):
        abrir_archivo(archivo_destino)

    boton_descargar_reservas = ft.ElevatedButton(
        text="Guardar reservas",
        on_click=descargar_reservas
    )

    boton_abrir_informe = ft.ElevatedButton(
        text="Abrir informe",
        on_click=abrir_informe
    )

    boton_regresar = ft.ElevatedButton(
        text="Regresar",
        on_click=lambda e: page.go("/")
    )

    contenido = ft.Column(
        [
            boton_descargar_reservas,
            boton_abrir_informe,
            boton_regresar
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    contenedor = ft.Container(
        content=contenido,
        alignment=ft.alignment.center,
        expand=True
    )

    page.add(contenedor)
    return ft.View("/admin", [contenedor])
