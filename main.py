import flet as ft
from registro import mostrar_registro, mostrar_consultar_reservas, mostrar_detalle_reserva
from admin import mostrar_admin

def mostrar_inicio(page: ft.Page):
    logo = ft.Image(
        src="assets/logo.png",
        width=250,
        height=250
    )
    
    boton_inicio = ft.ElevatedButton(
        text="Registrar Reserva", 
        on_click=lambda e: page.go("/registro")
    )
    
    boton_consultar = ft.ElevatedButton(
        text="Consultar Reservas",
        on_click=lambda e: page.go("/consultar")
    )

    boton_admin = ft.ElevatedButton(
        text="Administrar",
        on_click=lambda e: page.go("/admin")
    )
    
    inicio_contenido = ft.Column(
        [
            logo,
            boton_inicio,
            boton_consultar,
            boton_admin
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    return ft.View("/", [ft.Container(content=inicio_contenido, alignment=ft.alignment.center, expand=True)])

def main(page: ft.Page):
    page.title = "Sistema de Reservas"
    
    def route_change(event):
        route = event.route
        page.views.clear()
        if route == "/":
            page.views.append(mostrar_inicio(page))
        elif route == "/registro":
            page.views.append(mostrar_registro(page))
        elif route == "/consultar":
            page.views.append(mostrar_consultar_reservas(page))
        elif route.startswith("/detalle/"):
            reserva_id = route.split("/")[-1]
            page.views.append(mostrar_detalle_reserva(page, reserva_id))
        elif route == "/admin":
            page.views.append(mostrar_admin(page))
        page.update()
    
    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)