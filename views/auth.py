import flet as ft
from flet_core import padding
from flet_route import Params, Basket
import requests
import json


class SignUpComponent:
    def __init__(self, page: ft.Page):
        self.name_field = ft.TextField(label="Name", read_only=False)
        self.email_field = ft.TextField(label="Email", read_only=False)
        self.password_field = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            read_only=False,
            on_submit=lambda _: self.signup(page),
            hint_text="Password should be at least 8 characters",
        )
        self.save_button = ft.FilledButton(
            expand=True,
            text="Create Account",
            style=ft.ButtonStyle(
                # bgcolor=ft.colors.BLUE_50,
                shape={
                    ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=23),
                    ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                },
                padding=padding.all(2),
            ),
            height=55,
            width=100,
            on_click=lambda _: self.signup(page),
        )
        self.login_button = ft.TextButton(
            text="Already have an account? Log in here",
            expand=True,
            on_click=lambda _: page.go("/login"),
        )
        self.error_success_message = ft.Text(
            value="",
            font_family="DM Sans Medium",
            color=ft.colors.GREEN_700,
            size=25,
            visible=True,
        )

        self.signup_bs = ft.BottomSheet(
            content=ft.Container(
                # bgcolor=ft.colors.ORANGE_100,
                expand=True,
                alignment=ft.Alignment(0, 0),  # Center the Container itself
                content=ft.Column(
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center Column contents
                    alignment=ft.MainAxisAlignment.CENTER,  # Center Column vertically
                    controls=[
                        self.error_success_message,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.FilledButton(
                                    text="Login to account",
                                    style=ft.ButtonStyle(
                                        # bgcolor=ft.colors.LIGHT_BLUE_ACCENT_100,
                                        # color=ft.colors.WHITE,
                                        shape={
                                            ft.ControlState.HOVERED: ft.RoundedRectangleBorder(
                                                radius=23
                                            ),
                                            ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(
                                                radius=10
                                            ),
                                        },
                                        padding=padding.all(2),
                                    ),
                                    height=55,
                                    width=200,
                                    on_click=lambda _: page.go("/login"),
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        )
        self.signup_error_message = ft.Text(
            value="Server Error, please fill any missed fields",
            font_family="DM Sans Medium",
            color=ft.colors.ERROR,
            size=25,
            visible=True,
        )
        self.signup_error = ft.BottomSheet(
            content=ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),  # Center the Container itself
                content=ft.Column(
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center Column contents
                    alignment=ft.MainAxisAlignment.CENTER,  # Center Column vertically
                    controls=[self.signup_error_message],
                ),
            ),
        )

        self.loading_spinner = ft.ProgressRing(
            value=0, visible=False  # 0% - invisible initially
        )

    def signup(self, page: ft.Page):
        # self.save_button.disabled = True
        # page.update()

        page.add(self.loading_spinner)
        self.loading_spinner.visible = True
        page.update()

        name = self.name_field.value
        email = self.email_field.value
        password = self.password_field.value
        data = {"name": name, "email": email, "hashed_password": password}

        response = requests.post(
            url="https://password-manager-api-2ax5.onrender.com/v1/users/create",
            json=data,
        )
        self.loading_spinner.visible = False
        if response.status_code == 201:
            self.save_button.disabled = False
            self.error_success_message.value = "Successfully created!"
            self.signup_bs.open = True  # Explicitly open the BottomSheet
            page.add(self.signup_bs)
        if response.status_code == 409:
            # self.save_button.disabled = False
            # self.signup_error_message.value = "User with this email already exists!"
            # self.signup_error.open = True
            page.snack_bar = ft.SnackBar(
                ft.Text("User with this email already exists!"), bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
        elif response.status_code == 422:
            # self.save_button.disabled = False
            # self.signup_error_message.value = "Fill all fields!"
            # self.signup_error.open = True
            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Password should be greater that 8 character/ [Fill all the fields] !"
                ),
                bgcolor=ft.colors.RED,
            )
            page.snack_bar.open = True
            page.update()
        else:
            if response.status_code != 201:  # Handle unexpected errors only
                self.save_button.disabled = False
                self.signup_error_message.value = (
                    "An unexpected error occurred. Try again."
                )
                self.signup_error.open = True

        page.update()


class SignUpScreen:
    def __init__(self):
        self.name = "SignUpScreen"

    def view(self, page: ft.Page, params: Params, basket: Basket):

        signupComponents = SignUpComponent(page)

        signup_container = ft.Container(
            content=ft.Row(controls=[signupComponents.save_button])
        )
        login_container = ft.Container(
            content=ft.Row(controls=[signupComponents.login_button]),
        )

        form_container = ft.Container(
            padding=padding.only(top=30, bottom=10, left=10, right=10),
            content=ft.Column(
                spacing=20,
                controls=[
                    signupComponents.name_field,
                    signupComponents.email_field,
                    signupComponents.password_field,
                    signup_container,
                    login_container,
                ],
            ),
        )

        main_container = ft.Container(
            padding=padding.only(top=90),
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        value="Create a new account",
                        font_family="DM Sans Medium",
                        size=30,
                    ),
                    form_container,
                    signupComponents.signup_bs,
                    signupComponents.signup_error,
                    # signupComponents.error_message,
                ],
            ),
        )

        return ft.View(
            route="/signup",
            # padding=padding.only(left=23, right=23),
            spacing=0,
            controls=[main_container],
        )


class LoginComponent:
    def __init__(self, page: ft.Page, params: Params):
        self.email_field = ft.TextField(
            label="Email",
            autofill_hints=[ft.AutofillHint.EMAIL],
        )
        self.password_field = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            on_submit=lambda _: self.login(page),
        )

        self.create_account_button = ft.TextButton(
            text="Create an Account",
            expand=True,
            on_click=lambda _: page.go("/signup"),
        )
        self.loading_spinner = ft.ProgressRing(
            disabled=True, visible=False  # 0% - invisible initially
        )

        self.login_button = ft.FilledButton(
            expand=True,
            text="Login",
            style=ft.ButtonStyle(
                # bgcolor=ft.colors.BLUE_50,
                shape={
                    ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=23),
                    ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                },
                padding=padding.all(2),
            ),
            height=55,
            width=100,
            on_click=lambda _: self.login(page),
        )
        self.error_message = ft.Text(
            value="",
            font_family="DM Sans Medium",
            color=ft.colors.RED_700,
            size=25,
            visible=True,
        )

    def login(self, page):
        # self.login_button.disabled = True
        self.loading_spinner.disabled = False
        self.loading_spinner.visible = True
        page.update()

        email = self.email_field.value
        password = self.password_field.value

        data = {"username": email, "password": password}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            url="https://password-manager-api-2ax5.onrender.com/v1/auth/token",
            headers=headers,
            data=data,
        )

        if response.status_code == 200:
            response_dict = response.json()
            token_data = {
                "bearer_token": response_dict["access_token"],
                "user_id": response_dict["user_id"],
                "user_name": response_dict["user_name"],
                "user_email": email,
            }
            print(token_data)
            # basket.my_data = {
            #     "bearer_token": token_data,
            #     "user_id": response_dict["user_id"],
            #     "user_name": response_dict["user_name"],
            # }
            self.loading_spinner.visible = False
            with open("bearer_token.json", "w") as file:
                json.dump(token_data, file, indent=4)

            # with open("bearer_token.json", "r") as file:
            #     data = json.load(file)
            #     print("Bearer Token:", data["bearer_token"])

            # print("Success")
            page.snack_bar = ft.SnackBar(
                ft.Text("Login Success!"), bgcolor=ft.colors.GREEN
            )
            page.update()
            page.go("/home")
        elif response.status_code == 401:
            page.snack_bar = ft.SnackBar(
                ft.Text("Wrong username or password!"), bgcolor=ft.colors.RED
            )
            self.loading_spinner.visible = False
            page.snack_bar.open = True
            page.update()
        elif response.status_code == 404:
            page.snack_bar = ft.SnackBar(
                ft.Text("User Not found / Incomplete Field!"), bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            self.loading_spinner.visible = False

            page.update()
        else:
            self.loading_spinner.visible = False
            print("error", response.status_code)
            page.update()


class LoginScreen:
    def view(self, page: ft.Page, params: Params, basket: Basket):
        loginComponents = LoginComponent(page, params)

        login_Container = ft.Container(
            content=ft.Row(controls=[loginComponents.login_button])
        )
        create_acc_container = ft.Container(
            content=ft.Row(controls=[loginComponents.create_account_button])
        )

        form_container = ft.Container(
            padding=padding.only(top=30, bottom=10, left=10, right=10),
            content=ft.Column(
                spacing=20,
                controls=[
                    loginComponents.email_field,
                    loginComponents.password_field,
                    login_Container,
                    loginComponents.loading_spinner,
                    create_acc_container,
                ],
            ),
        )

        main_container = ft.Container(
            padding=padding.only(top=90),
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        value="Login to your account",
                        font_family="DM Sans Medium",
                        size=30,
                    ),
                    form_container,
                ],
            ),
        )
        return ft.View(
            route="/login",
            spacing=0,
            controls=[main_container],
        )
