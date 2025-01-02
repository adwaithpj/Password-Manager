import flet as ft
from flet_core import padding
from flet_route import Params, Basket
from middleware.refreshring import RefreshRequest
from middleware.token_check import TokenCheck
from threading import Thread


class RefreshScreen:
    def __init__(self):
        self.main_text = ft.Text(
            value="App is loading...",
            font_family="DM Sans Medium",
            size=30,
        )

    def check_server_and_route(self, page: ft.Page):
        def server_check():
            refresh_request = RefreshRequest()
            token_check = TokenCheck()
            result = refresh_request.run()

            # Update UI or navigate based on the result
            if result:
                self.main_text.value = "Checking Credentials"
                page.update()
                token_status = token_check.check()
                if token_status:
                    page.go("/home")
                else:
                    page.go("/login")
            else:
                # Show an error message or allow retry
                page.dialog = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("Failed to connect to the server."),
                    actions=[ft.TextButton("Retry", on_click=lambda _: page.go("/"))],
                )
                page.dialog.open = True
                page.update()

        # Run the server check in a background thread to avoid blocking the UI
        Thread(target=server_check).start()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        # UI for the loading screen

        ring = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,  # Vertically center the ring
            controls=[self.main_text, ft.ProgressRing()],
        )

        main_container = ft.Container(
            expand=True,
            padding=ft.padding.only(top=30),
            alignment=ft.alignment.center,  # Align content to the center of the container
            content=ring,  # Use `ring` as the main content
        )
        self.check_server_and_route(page)
        return ft.View(
            route="/",
            padding=ft.padding.only(left=23, right=23),
            spacing=0,
            controls=[main_container],
        )
