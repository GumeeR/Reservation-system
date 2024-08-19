import flet as ft
import pandas as pd
from datetime import datetime, timedelta

archivo_reservas = 'assets/reservas.xlsx'
archivo_usuarios = 'assets/usuarios.xlsx'

def cargar_reservas():
    try:
        df_reservas = pd.read_excel(archivo_reservas)
    except FileNotFoundError:
        df_reservas = pd.DataFrame(columns=['cedula', 'nombre', 'fecha_reserva', 'tipo_servicio', 'contratista', 'estado'])
    return df_reservas

def guardar_reservas(df_reservas):
    df_reservas.to_excel(archivo_reservas, index=False)

def cargar_usuarios():
    try:
        df_usuarios = pd.read_excel(archivo_usuarios)
    except FileNotFoundError:
        df_usuarios = pd.DataFrame(columns=['cedula', 'nombre', 'empresa'])
    return df_usuarios

def guardar_reserva(cedula, nombre, fecha_reserva, tipo_servicio, contratista):
    df_reservas = cargar_reservas()
    nueva_reserva = {
        'cedula': cedula,
        'nombre': nombre,
        'fecha_reserva': fecha_reserva,
        'tipo_servicio': tipo_servicio,
        'contratista': contratista,
        'estado': 'Activa'
    }
    df_reservas = pd.concat([df_reservas, pd.DataFrame([nueva_reserva])], ignore_index=True)
    guardar_reservas(df_reservas)

def mostrar_registro(page: ft.Page):
    fecha_actual = datetime.now() + timedelta(days=1)
    fecha_formateada = fecha_actual.strftime("%Y-%m-%d")
    
    cedula = ft.TextField(label="Cédula o Codigo", width=300)
    nombre_completo = ft.TextField(label="Nombre completo", width=300)
    fecha_reserva = ft.TextField(label="Fecha de reserva", value=fecha_formateada, width=300, disabled=True)
    
    tipo_servicio = ft.Dropdown(
        label="Tipo de servicio",
        options=[
            ft.dropdown.Option(key="Text1", text="Text1"),
            ft.dropdown.Option(key="Text2", text="Text2")
        ],
        width=300
    )
    
    contratista = ft.TextField(label="Contratista", width=300, disabled=True)

    cedula_sugerencias = ft.Dropdown(
        label="Sugerencias de Cédula",
        width=300,
        visible=False
    )
    
    nombre_sugerencias = ft.Dropdown(
        label="Sugerencias de Nombre",
        width=300,
        visible=False
    )

    df_usuarios = cargar_usuarios()

    def buscar_sugerencias_cedula(e):
        term = cedula.value
        if term:
            resultados = df_usuarios[df_usuarios['cedula'].astype(str).str.contains(term, na=False)].head(5)
            opciones = [ft.dropdown.Option(key=str(row['cedula']), text=f"{row['cedula']} - {row['nombre']}") for idx, row in resultados.iterrows()]
            cedula_sugerencias.options = opciones
            cedula_sugerencias.visible = True
            page.update()
        else:
            cedula_sugerencias.visible = False
            page.update()
    
    def seleccionar_cedula(e):
        if cedula_sugerencias.value:
            selected = df_usuarios[df_usuarios['cedula'] == int(cedula_sugerencias.value)]
            if not selected.empty:
                cedula.value = str(selected['cedula'].values[0])
                nombre_completo.value = selected['nombre'].values[0]
                contratista.value = selected['empresa'].values[0]
                page.update()
            cedula_sugerencias.visible = False
            page.update()

    cedula_sugerencias.on_change = seleccionar_cedula
    cedula.on_change = buscar_sugerencias_cedula

    def buscar_sugerencias_nombre(e):
        term = nombre_completo.value
        if term:
            resultados = df_usuarios[df_usuarios['nombre'].str.contains(term, na=False, case=False)].head(5)
            opciones = [ft.dropdown.Option(key=str(row['cedula']), text=f"{row['nombre']} - {row['cedula']}") for idx, row in resultados.iterrows()]
            nombre_sugerencias.options = opciones
            nombre_sugerencias.visible = True
            page.update()
        else:
            nombre_sugerencias.visible = False
            page.update()
    
    def seleccionar_nombre(e):
        if nombre_sugerencias.value:
            selected = df_usuarios[df_usuarios['cedula'] == int(nombre_sugerencias.value)]
            if not selected.empty:
                nombre_completo.value = selected['nombre'].values[0]
                cedula.value = str(selected['cedula'].values[0])
                contratista.value = selected['empresa'].values[0]
                page.update()
            nombre_sugerencias.visible = False
            page.update()

    nombre_sugerencias.on_change = seleccionar_nombre
    nombre_completo.on_change = buscar_sugerencias_nombre

    def generar_reserva(e):
        guardar_reserva(cedula.value, nombre_completo.value, fecha_reserva.value, tipo_servicio.value, contratista.value)
        
        cedula.value = ""
        nombre_completo.value = ""
        tipo_servicio.value = None
        contratista.value = ""
        fecha_reserva.value = fecha_formateada
        page.update()

    boton_generar_reserva = ft.ElevatedButton(
        text="Generar reserva", 
        on_click=generar_reserva
    )
    
    boton_regresar = ft.ElevatedButton(
        text="Regresar", 
        on_click=lambda e: page.go("/")
    )
    
    contenido = ft.Column(
        [
            cedula,
            cedula_sugerencias,
            nombre_completo,
            nombre_sugerencias,
            fecha_reserva,
            tipo_servicio,
            contratista,
            boton_generar_reserva,
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

    return ft.View("/registro", [contenedor])

def mostrar_consultar_reservas(page: ft.Page):
    df_reservas = cargar_reservas()
    reservas_activas = df_reservas[df_reservas['estado'] == 'Activa']

    lista_reservas = ft.ListView(expand=True, spacing=10)
    barra_busqueda = ft.TextField(
        label="Buscar por cédula",
        width=300,
        on_change=lambda e: actualizar_lista_reservas(e.control.value)
    )

    def actualizar_lista_reservas(busqueda: str):
        lista_reservas.controls.clear()
        reservas_filtradas = reservas_activas
        if busqueda:
            reservas_filtradas = reservas_activas[reservas_activas['cedula'].astype(str).str.contains(busqueda, na=False)]

        for idx, row in reservas_filtradas.iterrows():
            lista_reservas.controls.append(
                ft.ListTile(
                    title=ft.Text(row['nombre']),
                    subtitle=ft.Text(row['cedula']),
                    on_click=lambda e, idx=idx: page.go(f"/detalle/{idx}")
                )
            )
        page.update()

    actualizar_lista_reservas("")

    def regresar_a_inicio(e):
        page.go("/")

    boton_regresar = ft.ElevatedButton(
        text="Regresar",
        on_click=regresar_a_inicio
    )
    
    contenido = ft.Column(
        [
            barra_busqueda,
            lista_reservas,
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

    return ft.View("/consultar", [contenedor])

def mostrar_detalle_reserva(page: ft.Page, reserva_id):
    df_reservas = cargar_reservas()
    reserva = df_reservas.iloc[int(reserva_id)]

    cedula = ft.TextField(label="Cédula", value=reserva['cedula'], width=300, disabled=True)
    nombre_completo = ft.TextField(label="Nombre completo", value=reserva['nombre'], width=300, disabled=True)
    fecha_reserva = ft.TextField(label="Fecha de reserva", value=reserva['fecha_reserva'], width=300, disabled=True)
    tipo_servicio = ft.TextField(label="Tipo de servicio", value=reserva['tipo_servicio'], width=300, disabled=True)
    contratista = ft.TextField(label="Contratista", value=reserva['contratista'], width=300, disabled=True)

    def actualizar_estado(estado):
        df_reservas.at[int(reserva_id), 'estado'] = estado
        guardar_reservas(df_reservas)
        page.go("/consultar")

    boton_reserva_tomada = ft.ElevatedButton(
        text="Reserva tomada",
        on_click=lambda e: actualizar_estado('Tomada')
    )

    boton_reserva_no_tomada = ft.ElevatedButton(
        text="Reserva no tomada",
        on_click=lambda e: actualizar_estado('No tomada')
    )

    boton_regresar = ft.ElevatedButton(
        text="Regresar",
        on_click=lambda e: page.go("/consultar")
    )

    contenido = ft.Column(
        [
            cedula,
            nombre_completo,
            fecha_reserva,
            tipo_servicio,
            contratista,
            boton_reserva_tomada,
            boton_reserva_no_tomada,
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

    return ft.View(f"/detalle/{reserva_id}", [contenedor])