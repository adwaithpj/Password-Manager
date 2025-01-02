import flet as ft
from flet_route import Params, Basket
from middleware.delete import DeleteAccount


class UserProfile:
    def __init__(self):
        self.user_name = None
        self.user_email = None

    def view(self, page: ft.Page, params: Params, basket: Basket):

        details = basket.get("my_data")
        self.user_name = details["user_name"]
        self.user_email = details["user_email"]
        self.bearer_token = details["bearer_token"]
        self.id = details["user_id"]

        # Function to navigate back
        def go_back(e):
            page.go("/home")  # Change this to your desired route or logic

        # Function to delete the account
        def delete_account(e):
            confirmation_dialog.open = True
            page.update()

        # Function to handle confirmation of deletion
        def confirm_deletion(e):
            # Add your logic for account deletion (e.g., API call)
            # print("Account deleted!")
            confirmation_dialog.open = False
            del_middleware = DeleteAccount().delete_user(self.id, self.bearer_token)
            if del_middleware:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Account successfully deleted!"), bgcolor=ft.colors.GREEN
                )
                page.snack_bar.open = True
                page.update()
                page.go("/login")
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Unable to  delete at this moment, Try again Later!"),
                    bgcolor=ft.colors.RED,
                )
                page.snack_bar.open = True
                page.update()

        # Function to cancel deletion
        def cancel_deletion(e):
            confirmation_dialog.open = False
            page.update()

        # Confirmation Dialog
        confirmation_dialog = ft.AlertDialog(
            title=ft.Text("Confirm Account Deletion"),
            content=ft.Text(
                "Are you sure you want to delete your account? This action cannot be undone."
            ),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_deletion),
                ft.TextButton(
                    "Delete",
                    on_click=confirm_deletion,
                    style=ft.ButtonStyle(color=ft.colors.RED),
                ),
            ],
        )

        # Layout of the Profile Screen
        profile_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                tooltip="Back",
                                on_click=go_back,
                            ),
                            ft.Text("Profile", size=30, weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Divider(),
                    ft.Text(f"Name: {self.user_name}", size=18),
                    ft.Text(f"Email: {self.user_email}", size=18),
                    ft.Divider(),
                    ft.ElevatedButton(
                        "Delete Account",
                        icon=ft.icons.DELETE_OUTLINE,
                        style=ft.ButtonStyle(color=ft.colors.RED),
                        on_click=delete_account,
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(20),
        )

        page.dialog = confirmation_dialog
        return ft.View(route="/profile", controls=[profile_container])
