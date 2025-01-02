from math import e
import flet as ft
from flet_core import padding, popup_menu_button
from flet_route import Params, Basket
from views.create import HomeScreen
import json
from middleware.fetch_data import FetchData
from middleware.delete import DeleteData
from middleware.update import UpdateData


class MainScreen:
    def __init__(self):
        self.name = None
        self.bearer_token = None
        self.user_id = None
        self.selected_index = 0
        self.collect_personal_info()

        self.title_text = ft.Text(
            value="Password Manager",
            size=30,
            weight=ft.FontWeight.BOLD,
            font_family="DM Sans Medium",
            # color=ft.colors.BLACK
        )

    def collect_personal_info(self):
        try:
            with open("bearer_token.json", "r") as file:
                self.token_data = json.load(file)
                self.bearer_token = self.token_data["bearer_token"]
                self.name = self.token_data["user_name"]
                self.user_id = self.token_data["user_id"]
                self.user_email = self.token_data["user_email"]
        except FileNotFoundError:
            print("Could not find")

    def view(self, page: ft.Page, params: Params, basket: Basket):

        def update_password_list():
            # The code is adding a new password to a list called `self.password`.
            self.password = FetchData().fetch(self.bearer_token)

            _create_panel(self.password)  # Refresh the password panel
            # print(f"Password list updated: {}")
            page.update()

        # Fetching data
        self.collect_personal_info()
        hello = ft.Container(
            padding=padding.only(right=15),
            content=ft.Text(
                value=f"Hello, {self.name}",
                font_family="DM Sans Medium",
                weight=ft.FontWeight.BOLD,
                size=26,
            ),
        )

        def change_theme_color(e):
            selected_color = e.control.data
            page.theme = page.dark_theme = ft.theme.Theme(
                color_scheme=ft.ColorScheme.primary, color_scheme_seed=selected_color
            )
            page.update()

        theme_color_button = ft.PopupMenuButton(
            icon=ft.icons.COLOR_LENS_OUTLINED,
            tooltip="Change Theme Color",
            items=[
                ft.PopupMenuItem(
                    text="Deep Purple", data="deeppurple", on_click=change_theme_color
                ),
                ft.PopupMenuItem(
                    text="Indigo", data="indigo", on_click=change_theme_color
                ),
                ft.PopupMenuItem(
                    text="Blue (default)", data="blue", on_click=change_theme_color
                ),
                ft.PopupMenuItem(text="Teal", data="teal", on_click=change_theme_color),
                ft.PopupMenuItem(
                    text="Green", data="green", on_click=change_theme_color
                ),
                ft.PopupMenuItem(
                    text="Yellow", data="yellow", on_click=change_theme_color
                ),
                ft.PopupMenuItem(
                    text="Orange", data="orange", on_click=change_theme_color
                ),
                ft.PopupMenuItem(
                    text="Deep Orange", data="deeporange", on_click=change_theme_color
                ),
                ft.PopupMenuItem(text="Pink", data="pink", on_click=change_theme_color),
            ],
        )

        # Basket Logic Written below
        # Don't change this
        result = basket.get("my_data")
        if result is None:
            basket.my_data = {
                "bearer_token": self.bearer_token,
                "user_name": self.name,
                "user_id": self.user_id,
                "user_email": self.user_email,
            }
            result = basket.get("my_data")

        # fetching password after
        self.password = FetchData().fetch(self.bearer_token)

        # Create View
        create_screen = HomeScreen(on_password_saved=update_password_list).view(
            page, params, basket, bearer_token=self.bearer_token
        )

        # Dark Mode Function and Icon button
        def change_theme(e):
            if page.theme_mode == ft.ThemeMode.DARK:
                page.theme_mode = ft.ThemeMode.LIGHT

            else:
                page.theme_mode = ft.ThemeMode.DARK

            page.update()
            # time.sleep(0.5)
            self.toggledarklight.selected = not self.toggledarklight.selected
            page.update()

        self.toggledarklight = ft.IconButton(
            on_click=change_theme,
            icon_size=20,
            # content=ft.Text("Dark Mode",style=ft.TextStyle(color=ft.colors.SURFACE_VARIANT)),
            icon="light_mode",
            selected_icon="dark_mode",
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE, "selected": ft.colors.BLACK},
            ),
        )
        # self.change_theme =
        # Nav Bar Setup
        # Don change this

        def open_nav_drawer(e):
            page.end_drawer.open = True  # Assign the drawer to the page
            page.update()

        def on_dismiss_drawer(e):
            if self.selected_index == 1:
                e.control.selected_index = 1
            elif self.selected_index == 0:
                e.control.selected_index = 0
            page.update()

        # Navbar Changes
        def handle_nav_change(e):
            if e.control.selected_index == 0:
                # Home View
                page.title = "Home"
                self.selected_index = 0
                top_row.visible = True
                create_screen.visible = False
                create_screen.disabled = True
                homepage.visible = True
                page.update()
            elif e.control.selected_index == 1:
                # Create View
                page.title = "Create"
                self.selected_index = 1
                top_row.visible = False
                homepage.visible = False
                create_screen.visible = True
                create_screen.disabled = False
                page.update()
            elif e.control.selected_index == 2:
                # Menu Option - Open Navigation Drawer
                open_nav_drawer(e)

            page.update()

        # ----------------------------------------------------------------

        # Page Setup
        # Dont change this

        page.navigation_bar = ft.NavigationBar(
            on_change=handle_nav_change,
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.HOME, label="Home"),
                ft.NavigationBarDestination(icon=ft.icons.ADD, label="Add"),
                ft.NavigationBarDestination(
                    icon=ft.icons.MENU,
                    label="Options",
                ),
            ],
        )
        page.appbar = ft.AppBar(
            title=self.title_text,
            toolbar_height=80,
            bgcolor=ft.colors.SURFACE_VARIANT,
            center_title=True,
            actions=[self.toggledarklight, theme_color_button],
        )

        # Options Drawer for Profile and Logout

        # Logic for end_bar buttons

        def logout(e):
            try:
                with open("bearer_token.json", "w") as file1:
                    token_data = {
                        "bearer_token": " ",
                        "user_id": " ",
                        "user_name": " ",
                        "user_email": " ",
                    }
                    json.dump(token_data, file1, indent=4)
                file1.close()
                self.bearer_token = None
                self.password = None
                page.clean()
                page.update()
                page.remove()
                page.go("/login")

            except FileNotFoundError:
                print("Could not find")

        page.end_drawer = ft.NavigationDrawer(
            on_dismiss=on_dismiss_drawer,
            controls=[
                ft.Container(
                    # bgcolor=ft.colors.GREEN,
                    padding=ft.padding.all(20),
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.FilledButton(
                                        expand=True,
                                        icon=ft.icons.PERSON,
                                        text="Profile",
                                        on_click=lambda _: page.go("/profile"),
                                        style=ft.ButtonStyle(
                                            shape={
                                                ft.ControlState.HOVERED: ft.RoundedRectangleBorder(
                                                    radius=23
                                                ),
                                                ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(
                                                    radius=10
                                                ),
                                            },
                                            padding=padding.all(30),
                                        ),
                                    ),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.FilledTonalButton(
                                        expand=True,
                                        on_click=logout,
                                        icon=ft.icons.LOGOUT,
                                        text="Logout",
                                        style=ft.ButtonStyle(
                                            shape={
                                                ft.ControlState.HOVERED: ft.RoundedRectangleBorder(
                                                    radius=23
                                                ),
                                                ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(
                                                    radius=10
                                                ),
                                            },
                                            padding=padding.all(30),
                                        ),
                                    ),
                                ]
                            ),
                        ],
                    ),
                )
            ],
        )
        ################################

        def _create_panel(password_list):
            panel.controls.clear()

            for pwd in password_list:
                if isinstance(pwd, dict):
                    panel.controls.append(
                        ft.ExpansionPanel(
                            header=ft.ListTile(
                                title=ft.Text(
                                    value=f"{pwd['website_name']}",
                                    font_family="DM Sans Medium",
                                    size=20,
                                    weight=ft.FontWeight.W_500,
                                ),
                                trailing=ft.Icon(ft.icons.LOCK),
                            ),
                            content=ft.Container(
                                padding=ft.padding.all(10),
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Text(
                                                    f"Username: {pwd['username_email']}",
                                                    font_family="DM Sans Medium",
                                                    size=20,
                                                ),
                                                ft.IconButton(
                                                    icon=ft.icons.COPY,
                                                    on_click=lambda e, text=pwd[
                                                        "username_email"
                                                    ]: page.set_clipboard(
                                                        text
                                                    ),  # pyperclip.copy(text),
                                                ),
                                            ]
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.Text(
                                                    f"Password: {pwd['password']}",
                                                    font_family="DM Sans Medium",
                                                    size=20,
                                                ),
                                                ft.IconButton(
                                                    icon=ft.icons.COPY,
                                                    on_click=lambda e, text=pwd[
                                                        "password"
                                                    ]: page.set_clipboard(text),
                                                ),
                                            ]
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.IconButton(
                                                    icon=ft.icons.DELETE,
                                                    on_click=lambda e, id=pwd[
                                                        "id"
                                                    ]: delete(id),
                                                    style=ft.ButtonStyle(
                                                        color=ft.colors.RED
                                                    ),
                                                ),
                                                ft.IconButton(
                                                    icon=ft.icons.EDIT,
                                                    on_click=lambda e, pwd=pwd: update_password(
                                                        pwd
                                                    ),
                                                ),
                                            ]
                                        ),
                                    ],
                                    spacing=10,
                                ),
                            ),
                        )
                    )
            page.update()

        def delete(id):
            del_middleware = DeleteData().delete_pass(id, self.bearer_token)
            if del_middleware:
                self.password = [pwd for pwd in self.password if pwd["id"] != id]
                _create_panel(self.password)
                page.snack_bar = ft.SnackBar(
                    ft.Text("Password deleted successfully!"), bgcolor=ft.colors.GREEN
                )
                page.snack_bar.open = True
                page.update()
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Session Expired!Logging Out"), bgcolor=ft.colors.RED
                )
                page.snack_bar.open = True
                page.update()
                page.go("/login")

        def update(id, data, page):
            data1 = json.dumps(data)
            print(data)
            update_middleware = UpdateData().patch_pass(id, self.bearer_token, data1)
            if update_middleware:
                for pwd in self.password:
                    if pwd["id"] == id:
                        pwd["username_email"] = data["username_email"]
                        pwd["password"] = data["password"]
                        break
                _create_panel(self.password)
                page.snack_bar = ft.SnackBar(
                    ft.Text("Password was updated successfully!"),
                    bgcolor=ft.colors.GREEN,
                )
                page.snack_bar.open = True
                page.dialog.open = False
                page.update()
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Session Expired!Logging Out"), bgcolor=ft.colors.RED
                )
                page.snack_bar.open = True
                page.dialog.open = False
                page.update()
                page.go("/login")

        def close_dialog(page):
            page.dialog.open = False
            page.update()

        def update_password(pwd):
            # Placeholder for password update logic
            website_patch_name = ft.TextField(
                label="Website", value=pwd["website_name"], disabled=True
            )
            password_patch = ft.TextField(
                label="Password",
                value=pwd["password"],
                min_lines=8,
                on_change=lambda e: check_changes(),
            )
            username_patch = ft.TextField(
                label="Username",
                value=pwd["username_email"],
                on_change=lambda e: check_changes(),
            )

            save_button = ft.TextButton(
                "Save",
                disabled=True,
                on_click=lambda e: update(
                    pwd["id"],
                    data={
                        "username_email": username_patch.value,
                        "password": password_patch.value,
                    },
                    page=page,
                ),
            )

            def check_changes():
                if (
                    username_patch.value != pwd["username_email"]
                    or password_patch.value != pwd["password"]
                ):
                    save_button.disabled = False
                else:
                    save_button.disabled = True
                page.update()

            page.dialog = ft.AlertDialog(
                title=ft.Text("Update Password"),
                content=ft.Column(
                    controls=[
                        website_patch_name,
                        username_patch,
                        password_patch,
                    ]
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=lambda _: close_dialog(page)),
                    save_button,
                ],
            )
            page.dialog.open = True
            page.update()

        def update_filtered_list(e):
            search_text = e.control.value.lower()
            filtered_passwords = [
                pwd
                for pwd in self.password
                if search_text in pwd["website_name"].lower()
            ]
            _create_panel(filtered_passwords)

        search_bar = ft.TextField(
            hint_text="Search",
            on_change=update_filtered_list,
            prefix_icon=ft.icons.SEARCH,
            width=130,
            height=45,
        )

        panel = ft.ExpansionPanelList(
            elevation=8,
            divider_color=ft.colors.AMBER,
        )

        _create_panel(self.password)
        top_row = ft.Container(
            # padding=ft.padding.symmetric(horizontal=10),
            padding=ft.padding.all(10),
            content=ft.Row(
                spacing=80,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                tight=False,
                # expand=True,
                controls=[
                    hello,
                    search_bar,
                ],
            ),
        )
        listContainer = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[panel],
        )

        # Home Screen List Container
        homeScreenContainer = ft.Container(
            padding=ft.padding.all(10),
            border_radius=ft.border_radius.all(10),
            content=listContainer,
        )

        # Main Home Page
        # Don't Change this!!
        homepage = ft.Pagelet(
            expand=True,
            content=homeScreenContainer,
            # bgcolor=ft.colors.AMBER_100,
            # height=440,
        )

        # Main Container of Home Page
        # This has both list page and create screen from create.py
        # main_container = ft.Container(
        #     content=ft.Column(controls=[top_row, homepage, create_screen], expand=True)
        # )

        return ft.View(
            route="/home",
            end_drawer=page.end_drawer,
            appbar=page.appbar,
            controls=[
                page.appbar,
                # main_container,
                top_row,
                homepage,
                create_screen,
                page.navigation_bar,
                page.end_drawer,
            ],
        )
