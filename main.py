import flet as ft
from flet_route import Params,Basket,Routing,path
from views.home import HomeScreen
from jsondic import JsonDict

def main(page: ft.Page):
    app_routes = [
        path(
            url='/',
            clear=True,
            view=HomeScreen().view
        )
    ]
    Routing(page=page, app_routes=app_routes)
    page.theme_mode = ft.ThemeMode.LIGHT

    page.window_min_width = 480
    page.window_max_width = 1280
    page.window_min_height = 720
    page.window_max_height = 720
    page.fonts = {
        "DM Sans regular": "assets/google_fonts/dmsans_static/DMSans-Regular.ttf",
        "DM Sans Bold": "assets/google_fonts/dmsans_static/DMSans-Bold.ttf",
        "DM Sans Italic": "assets/google_fonts/dmsans_static/DMSans-Italic.ttf",  # Add other weights and styles
        "DM Sans Bold Italic": "assets/google_fonts/dmsans_static/DMSans-BoldItalic.ttf",
        "DM Sans Medium": "assets/google_fonts/dmsans_static/DMSans-Medium.ttf",
        "DM Sans Medium Italic": "assets/google_fonts/dmsans_static/DMSans-MediumItalic.ttf",
        "DM Sans SemiBold": "assets/google_fonts/dmsans_static/DMSans-SemiBold.ttf",
        "DM Sans SemiBold Italic": "assets/google_fonts/dmsans_static/DMSans-SemiBoldItalic.ttf",
        "DM Sans Light": "assets/google_fonts/dmsans_static/DMSans-Light.ttf",
        "DM Sans Light Italic": "assets/google_fonts/dmsans_static/DMSans-LightItalic.ttf",
        "DM Sans ExtraLight": "assets/google_fonts/dmsans_static/DMSans-ExtraLight.ttf",
        "DM Sans ExtraLight Italic": "assets/google_fonts/dmsans_static/DMSans-ExtraLightItalic.ttf",
        "DM Sans Thin": "assets/google_fonts/dmsans_static/DMSans-Thin.ttf",
        "DM Sans Thin Italic": "assets/google_fonts/dmsans_static/DMSans-ThinItalic.ttf",

    }
    page.go(page.route)

ft.app(target=main)
