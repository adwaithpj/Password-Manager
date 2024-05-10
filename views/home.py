import time

import flet as ft
from flet_core import padding
from flet_route import Params, Basket
from jsondic import JsonDict
import random
import string
import json
import pyperclip

class HomeScreen:

    def __init__(self):
        self.appbar_cont = None
        self.toggledarklight = None
        self.pass_cont = None
        self.website_cont = None
        self.gen_button = None
        self.search_button = None
        self.contact = None
        self.side_bar = None
        self.home_pagelet = None

        self.ref_websitename = ft.Ref[ft.TextField]()
        self.ref_email = ft.Ref[ft.TextField]()
        self.ref_password = ft.Ref[ft.TextField]()
        self.website_textf = ft.TextField(ref=self.ref_websitename, label="Website Name", width=380, height=55,
                                          text_align=ft.TextAlign.LEFT, enable_suggestions=True, expand=True)
        self.email_textf = ft.TextField(ref=self.ref_email, label="Email ID", height=55,
                                        text_align=ft.TextAlign.LEFT)
        self.password_textf = ft.TextField(ref=self.ref_password, label="Password", password=True,
                                           can_reveal_password=True, height=55, expand=True)



    def view(self, page: ft.Page, params: Params, basket: Basket):


        def show_banner(e):
            page.banner.open = True
            page.update()
        def close_banner(e):
            page.banner.open = False
            page.update()

        save_banner = ft.Banner(
            bgcolor=ft.colors.GREEN_200,
            leading=ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINED, size=40),
            content=ft.Text(
                "Password Saved!",
                font_family="DM Sans Medium",
                size=15,
            ),
            actions=[
                ft.TextButton("Close", on_click=close_banner),

            ],
        )
        page.banner = save_banner
        def generate_password(e):
            length = 12
            characters = string.ascii_letters + string.digits + string.punctuation
            pass_word = ''.join(random.choice(characters) for _ in range(length))
            self.password_textf.value = pass_word
            page.update()
            pyperclip.copy(pass_word)


        self.save_result_email = ft.TextField(
            value="",
            label='Email',
            expand=True,
        )
        self.save_result_pass= ft.TextField(
            value="",
            expand=True,
            label='Password'
        )
        def show_ss(e):

            ss.open = True
            page.overlay.append(ss)
            page.update()

        def close_ss(e):
            ss.open = False
            page.update()


        ss = ft.BottomSheet(
            content=ft.Container(

                alignment=ft.Alignment(0, 1),
                expand=True,
                height=240,
                padding=20,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    # alignment=ft.MainAxisAlignment.CENTER,
                    spacing=18,
                    controls=
                    [
                        ft.Text(
                            value="Saved Password!",
                            font_family="DM Sans Medium",
                            size=20,
                        ),
                        ft.Row(
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                self.save_result_email,
                                ft.IconButton(
                                    icon='content_copy',
                                    tooltip='Copy Email',
                                    on_click=lambda e: pyperclip.copy(self.save_result_email.value)
                                )

                            ]
                        ),
                        ft.Row(
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                self.save_result_pass,
                                ft.IconButton(
                                    icon='content_copy',
                                    tooltip='Copy Password',
                                    on_click=lambda e: pyperclip.copy(self.save_result_pass.value)
                                )

                            ]
                        )

                    ],

                ),

            ),
            open=True,

        )

        def save_password(_):
            print(self.website_textf.value)
            website_data = str(self.website_textf.value)
            email_or_username_data = str(self.email_textf.value)
            password_data = str(self.password_textf.value)
            print(website_data)
            # Check if all required fields are provided before saving
            if website_data and email_or_username_data and password_data:
                # is_ok = messagebox.askokcancel(title=website_data,
                #                                message=f"These are the details entered: \nEmail: {email_or_username_data}\nPassword: {password_data}\nIs it ok to save?")
                # if is_ok:
                # --------------------------------- JSON SAVE FILE ---------------------------------#
                json_data = JsonDict(website_data, email_or_username_data, password_data)
            else:
                if not website_data:
                    pass
                if not email_or_username_data:
                    pass
                if not password_data:
                    pass
        def search_password(e):
            website_to_search = self.website_textf.value

            try:
                with open('pass.json', 'r') as json_file:
                    data = json.load(json_file)
                    if website_to_search in data:
                        print_email = data[website_to_search]["email"]
                        print_password = data[website_to_search]["password"]
                        self.save_result_email.value = print_email
                        print_password = JsonDict.decode_password(JsonDict, print_password)
                        self.save_result_pass.value = print_password
                        page.update()
                        show_ss(e)

                        # messagebox.showinfo(title=website_to_search,
                        #                     message=f"Email: {print_email}\nPassword: {print_password}")
                    else:
                        pass
            except FileNotFoundError:
                pass

        def bs_dismissed(e):
            print("Dismissed!")

        def bs_call(e):
            bs.open = False
            page.update()
            save_password(" ")
            show_banner(e)
            page.update()
            self.password_textf.value = ""
            self.website_textf.value = ""
            self.email_textf.value = ""
            page.update()
            time.sleep(2.5)
            close_banner(e)
            page.update()

        def check_web(e):
            if self.website_textf.value == "":
                self.website_textf.border_color = 'red'
                page.update()
            else:
                self.website_textf.border_color = 'dark'
                show_bs(e)
        def show_bs(e):

            bs.open = True
            page.overlay.append(bs)
            page.update()

        def close_bs(e):
            bs.open = False
            page.update()

        bs = ft.BottomSheet(
            content=ft.Container(
                alignment=ft.Alignment(0, 1),
                expand=True,
                height=150,
                padding=padding.only(top=20),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    # alignment=ft.MainAxisAlignment.CENTER,
                    spacing=18,
                    controls=
                    [
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
                                    "Cancel", on_click=close_bs,
                                    style=ft.ButtonStyle(
                                        shape={
                                            ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=15),
                                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                                        },
                                        padding=padding.all(2),
                                    ),
                                    width=115,
                                    height=45
                                ),
                                ft.FilledButton(
                                    "Confirm", on_click=bs_call,
                                    style=ft.ButtonStyle(
                                        shape={
                                            ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=15),
                                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                                        },
                                        padding=padding.all(2),
                                    ),
                                    width=115,
                                    height=45
                                ),
                            ]
                        )
                    ],

                ),

            ),
            open=True,
            on_dismiss=bs_dismissed,
        )

        def save_prog(e):
            page.overlay.append(bs)
            page.update()
            show_bs(e)

        self.side_bar = ft.Container(
            bgcolor='#4848fa',
            width=50,
            content=ft.Text(
                value='Logo',
                color='white',
                size=20,
                weight=ft.FontWeight.BOLD
            )
        )
        self.search_button = ft.FloatingActionButton(
            icon="search",
            tooltip='Search for saved password',
            on_click=search_password,
        )
        self.gen_button = ft.FilledTonalButton(
            text="Generate",
            on_click=generate_password,
            tooltip='Generate a random password',
            style=ft.ButtonStyle(
                shape={
                    ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=15),
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                },
                padding=padding.all(2),

            ),
            width=106.5,
            height=55

        )

        self.website_cont = ft.Container(
            ft.Row(
                controls=[
                    self.website_textf,
                    self.search_button
                ]
            )
            # bgcolor='grey',
        )

        self.pass_cont = ft.Container(
            content=ft.Row(
                controls=[
                    self.password_textf,
                    self.gen_button
                ]
            )
        )

        def change_theme(e):
            if page.theme_mode == "dark":
                page.theme_mode = "light"

                self.password_textf.border_color = 'light'
            else:
                page.theme_mode = "dark"
                self.password_textf.border_color = 'dark'

            page.update()
            # time.sleep(0.5)
            self.toggledarklight.selected = not self.toggledarklight.selected
            page.update()

        self.toggledarklight = ft.IconButton(
            on_click=change_theme,
            icon_size=20,
            # content=ft.Text("Dark Mode",style=ft.TextStyle(color=ft.colors.SURFACE_VARIANT)),
            icon='dark_mode',
            selected_icon='light_mode',
            style=ft.ButtonStyle(
                color={"": ft.colors.BLACK, "selected": ft.colors.WHITE},

            )
        )
        self.contact = ft.IconButton(
            icon=ft.icons.QUESTION_MARK_ROUNDED,
            icon_size=20,
            tooltip='Contact Us',
            selected_icon='light_mode',

        )
        self.title_text = ft.Text(
            value="Password Manager",
            size=30,
            weight=ft.FontWeight.BOLD,
            font_family='DM Sans Medium',
            # color=ft.colors.BLACK
        )
        self.appbar_cont = ft.AppBar(
            title=self.title_text,

            toolbar_height=80,
            bgcolor=ft.colors.SURFACE_VARIANT,
            center_title=True,
            actions=[
                self.toggledarklight,
                self.contact
            ]

        )
        self.save_button = ft.FilledButton(
            expand=True,
            text='Save',
            style=ft.ButtonStyle(
                # bgcolor=ft.colors.BLUE_50,

                shape={
                    ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=23),
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                },
                padding=padding.all(2),

            ),

            height=55,
            on_click=check_web

        )

        self.save_cont = ft.Container(
            content=ft.Row(
                controls=[
                    self.save_button
                ]
            )
        )


        return ft.View(
            '/',
            padding=padding.only(left=23, right=23),
            spacing=0,
            controls=[

                self.appbar_cont,

                ft.Container(
                    padding=padding.only(top=30),
                    content=ft.Column(
                        expand=True,
                        # alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                value='Guard, Manage, Secure',
                                font_family='DM Sans Medium',
                                size=20,
                            ),
                            ft.Text(
                                value='Add new password or Search for saved passwords',
                                font_family='DM Sans light',
                                size=13
                            ),
                            ft.Container(
                                padding=padding.only(top=30, bottom=10, left=10, right=10),
                                content=ft.Column(
                                    spacing=20,
                                    controls=[
                                        self.website_cont,
                                        self.email_textf,
                                        self.pass_cont,
                                        self.save_cont
                                    ]

                                )
                            ),
                            ft.Container(
                                padding=padding.only(top=50),
                                alignment=ft.Alignment(0, 1),
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            "© 2024 Adwaith PJ"
                                        ),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.CircleAvatar(
                                                    foreground_image_url='https://img.freepik.com/premium-vector/new-twitter-logo-x-2023-twitter-x-logo-vector-download_691560-10794.jpg',
                                                    scale=0.5
                                                ),
                                                ft.CircleAvatar(
                                                    foreground_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png',
                                                    scale=0.5,

                                                ),
                                                ft.CircleAvatar(
                                                    foreground_image_url='https://cdn-icons-png.flaticon.com/512/25/25231.png',
                                                    scale=0.5
                                                ),
                                            ]
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )

            ]
        )
