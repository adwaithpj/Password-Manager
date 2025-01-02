import time
import random
import string
import json
import flet as ft
from flet_core import padding
from flet_route import Params, Basket
from middleware.add import AddPassword


class HomeScreen:
    def __init__(self, on_password_saved=None):
        self._initialize_references()
        self._create_text_fields()
        self.on_password_saved = on_password_saved

    def _initialize_references(self):
        self.appbar_cont = None
        self.toggledarklight = None
        self.pass_cont = None
        self.website_cont = None
        self.gen_button = None
        self.search_button = None
        self.contact = None
        self.side_bar = None
        self.home_pagelet = None
        self.bearer_token = None

        self.ref_websitename = ft.Ref[ft.TextField]()
        self.ref_email = ft.Ref[ft.TextField]()
        self.ref_password = ft.Ref[ft.TextField]()

    def _create_text_fields(self):
        self.website_textf = ft.TextField(
            ref=self.ref_websitename,
            label="Website Name",
            width=380,
            height=55,
            text_align=ft.TextAlign.LEFT,
            enable_suggestions=True,
            expand=True,
        )
        self.email_textf = ft.TextField(
            ref=self.ref_email,
            label="Email ID",
            height=55,
            text_align=ft.TextAlign.LEFT,
        )
        self.password_textf = ft.TextField(
            ref=self.ref_password,
            label="Password",
            password=True,
            can_reveal_password=True,
            height=55,
            expand=True,
        )

    def view(self, page: ft.Page, params: Params, basket: Basket, bearer_token):
        self._setup_navigation_bar(page)
        # self._setup_save_banner(page)
        self._setup_save_result_fields()
        self.bearer_token = bearer_token

        def generate_password(e):
            length = 12
            characters = string.ascii_letters + string.digits + string.punctuation
            pass_word = "".join(random.choice(characters) for _ in range(length))
            self.password_textf.value = pass_word
            page.update()
            page.set_clipboard(pass_word)

        def save_password(_):
            website_data = str(self.website_textf.value)
            email_or_username_data = str(self.email_textf.value)
            password_data = str(self.password_textf.value)

            if website_data and email_or_username_data and password_data:
                # JsonDict(website_data, email_or_username_data, password_data)
                data = {
                    "website_name": website_data,
                    "username_email": email_or_username_data,
                    "password": password_data,
                }
                add_middleware = AddPassword().add(
                    data=data, bearer_token=self.bearer_token
                )
                if add_middleware.status_code == 201:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Password Added successfully!"), bgcolor=ft.colors.GREEN
                    )
                    if self.on_password_saved:
                        self.on_password_saved()
                    page.snack_bar.open = True
                    page.update()
                elif add_middleware.status_code == 422:
                    page.snack_bar = ft.SnackBar(ft.Text("Fill all the fields!"))
                    page.snack_bar.open = True
                    page.update()
                else:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Server Error! Please try again"), bgcolor=ft.colors.RED
                    )
                    page.snack_bar.open = True
                    page.update()

        self._setup_bottom_sheets(page, save_password)
        self._create_ui_components(page, generate_password)

        return self._create_main_container(page)

    def _setup_navigation_bar(self, page):
        def handle_nav_change(e):
            titles = {0: "Explore!", 1: "Commute!", 2: "Bookmark!"}
            page.title = titles.get(e.control.selected_index, "")
            page.controls = (
                [ft.Text(page.title)] if e.control.selected_index != 0 else []
            )
            page.update()

        page.navigation_bar = ft.NavigationBar(
            on_change=handle_nav_change,
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
                ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Commute"),
                ft.NavigationBarDestination(
                    icon=ft.icons.BOOKMARK_BORDER,
                    selected_icon=ft.icons.BOOKMARK,
                    label="Bookmark",
                ),
            ],
        )

    def _setup_save_result_fields(self):
        self.save_result_email = ft.TextField(
            value="",
            label="Email",
            expand=True,
        )
        self.save_result_pass = ft.TextField(value="", label="Password", expand=True)

    def _setup_bottom_sheets(self, page, save_password):
        def bs_call(e):
            self.bottom_sheet.open = False
            page.update()
            save_password(" ")
            page.update()

            # Clear input fields
            for field in [self.password_textf, self.website_textf, self.email_textf]:
                field.value = ""
            page.update()

            time.sleep(2.5)
            page.update()

        def check_web(e):
            self.website_textf.border_color = (
                "red" if not self.website_textf.value else "dark"
            )
            self.password_textf.border_color = (
                "red" if not self.password_textf.value else "dark"
            )
            self.email_textf.border_color = (
                "red" if not self.email_textf.value else "dark"
            )
            page.update()
            if (
                self.website_textf.value
                and self.password_textf.value
                and self.email_textf.value
            ):
                self._show_confirmation_sheet(page, bs_call)

        self.save_button = ft.FilledButton(
            expand=True,
            text="Save",
            style=ft.ButtonStyle(
                shape={
                    ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=23),
                    ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                },
                padding=padding.all(2),
            ),
            height=55,
            on_click=check_web,
        )

    def _show_confirmation_sheet(self, page, confirm_action):
        confirm_sheet = ft.BottomSheet(
            content=ft.Container(
                alignment=ft.Alignment(0, 1),
                expand=True,
                height=150,
                padding=padding.only(top=20),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=18,
                    controls=[
                        ft.Text(
                            value="Confirm Before Saving?",
                            font_family="DM Sans Medium",
                            size=20,
                        ),
                        ft.Row(
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.OutlinedButton(
                                    "Cancel",
                                    on_click=lambda e: self._close_sheet(page),
                                    width=115,
                                    height=45,
                                ),
                                ft.FilledButton(
                                    "Confirm",
                                    on_click=confirm_action,
                                    width=115,
                                    height=45,
                                ),
                            ],
                        ),
                    ],
                ),
            ),
            open=True,
        )
        self.bottom_sheet = confirm_sheet
        page.overlay.append(confirm_sheet)
        page.update()

    def _close_sheet(self, page):
        self.bottom_sheet.open = False
        page.update()

    # def _show_saved_sheet(self, page):
    #     saved_sheet = ft.BottomSheet(
    #         content=ft.Container(
    #             alignment=ft.Alignment(0, 1),
    #             expand=True,
    #             height=240,
    #             padding=20,
    #             content=ft.Column(
    #                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    #                 spacing=18,
    #                 controls=[
    #                     ft.Text(
    #                         value="Saved Password!",
    #                         font_family="DM Sans Medium",
    #                         size=20,
    #                     ),
    #                     ft.Row(
    #                         spacing=20,
    #                         alignment=ft.MainAxisAlignment.CENTER,
    #                         controls=[
    #                             self.save_result_email,
    #                             ft.IconButton(
    #                                 icon="content_copy",
    #                                 tooltip="Copy Email",
    #                                 on_click=lambda e: pyperclip.copy(
    #                                     self.save_result_email.value
    #                                 ),
    #                             ),
    #                         ],
    #                     ),
    #                     ft.Row(
    #                         spacing=20,
    #                         alignment=ft.MainAxisAlignment.CENTER,
    #                         controls=[
    #                             self.save_result_pass,
    #                             ft.IconButton(
    #                                 icon="content_copy",
    #                                 tooltip="Copy Password",
    #                                 on_click=lambda e: pyperclip.copy(
    #                                     self.save_result_pass.value
    #                                 ),
    #                             ),
    #                         ],
    #                     ),
    #                 ],
    #             ),
    #         ),
    #         open=True,
    #     )
    #     page.overlay.append(saved_sheet)
    #     page.update()

    def _create_ui_components(self, page, generate_password):
        def change_theme(e):
            page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
            self.password_textf.border_color = (
                "light" if page.theme_mode == "light" else "dark"
            )
            page.update()
            self.toggledarklight.selected = not self.toggledarklight.selected
            page.update()

        self.toggledarklight = ft.IconButton(
            on_click=change_theme,
            icon_size=20,
            icon="dark_mode",
            selected_icon="light_mode",
            style=ft.ButtonStyle(
                color={"": ft.colors.BLACK, "selected": ft.colors.WHITE},
            ),
        )

        self.contact = ft.IconButton(
            icon=ft.icons.QUESTION_MARK_ROUNDED,
            icon_size=20,
            tooltip="Contact Us",
        )

        self.title_text = ft.Text(
            value="Password Manager",
            size=30,
            weight=ft.FontWeight.BOLD,
            font_family="DM Sans Medium",
        )

        self.appbar_cont = ft.AppBar(
            title=self.title_text,
            toolbar_height=80,
            bgcolor=ft.colors.SURFACE_VARIANT,
            center_title=True,
            actions=[self.toggledarklight, self.contact],
        )

        self.gen_button = ft.FilledTonalButton(
            text="Generate",
            on_click=generate_password,
            tooltip="Generate a random password",
            height=55,
            style=ft.ButtonStyle(
                shape={
                    ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=23),
                    ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                },
            ),
        )

        self.website_cont = ft.Container(content=ft.Row(controls=[self.website_textf]))

        self.pass_cont = ft.Container(
            content=ft.Row(controls=[self.password_textf, self.gen_button])
        )

    def _create_main_container(self, page):
        return ft.Container(
            visible=False,
            disabled=True,
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=padding.only(top=30),
                        content=ft.Column(
                            expand=True,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    value="Guard, Manage & Secure",
                                    font_family="DM Sans Medium",
                                    size=20,
                                ),
                                ft.Text(
                                    value="Add new password or Search for saved passwords",
                                    font_family="DM Sans light",
                                    size=13,
                                ),
                                ft.Container(
                                    padding=padding.only(
                                        top=30, bottom=10, left=10, right=10
                                    ),
                                    content=ft.Column(
                                        spacing=20,
                                        controls=[
                                            self.website_cont,
                                            self.email_textf,
                                            self.pass_cont,
                                            ft.Container(
                                                content=ft.Row(
                                                    controls=[self.save_button]
                                                )
                                            ),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    padding=padding.only(top=50),
                                    alignment=ft.Alignment(0, 1),
                                    content=ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text("© 2024 Adwaith PJ"),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )
