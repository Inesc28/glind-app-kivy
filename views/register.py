from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from backend.users import register_new_user
from views.login_view import LoginScreen

class RegisterScreen(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 20

        # Crear el logo
        self.logo = Image(
            source="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/3044f73c-0547-4b01-aeec-7ebff6555e1b/dj1p9o7-af65f7df-e4ef-497f-9cb7-b4545d76045e.png/v1/fill/w_400,h_400/logo_glind_by_coloringdancingedits_dj1p9o7-fullview.png",
            size_hint=(None, None),
            size=(120, 160)
        )
        self.add_widget(self.logo)

        # Crear el título
        self.title = Label(
            text="Regístrate",
            font_size='24sp',
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.title)

        # Crear los campos de texto
        self.email = TextInput(
            hint_text="Email",
            multiline=False,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.email)

        self.user = TextInput(
            hint_text="Username",
            multiline=False,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.user)

        self.password = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.password)

        # Crear el botón de registro
        self.save_button = Button(
            text="Registrar",
            size_hint=(1, None),
            height=40,
            background_color=(0.6, 0.2, 0.8, 1)
        )
        self.save_button.bind(on_release=self.register_data)
        self.add_widget(self.save_button)

        # Crear el botón de iniciar sesión
        self.log_button = Button(
            text="Si ya tienes una cuenta, Inicia Sesión",
            size_hint=(1, None),
            height=40,
            background_color=(0.6, 0.2, 0.8, 1)
        )
        self.log_button.bind(on_release=self.handle_register)
        self.add_widget(self.log_button)

    def register_data(self, instance):
        register_new_user(self.email.text, self.user.text, self.password.text)
        self.handle_register(instance)

    def handle_register(self, instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(LoginScreen())
