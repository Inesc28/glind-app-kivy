import requests
from io import BytesIO
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.core.image import Image as CoreImage
from backend.users import register_new_user
from views.login_view import LoginScreen


Builder.load_file('styles.kv')
class ButtonLogin(Button):
    pass

class RegisterScreen(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 20
        
        logo_url = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/3044f73c-0547-4b01-aeec-7ebff6555e1b/dj1p9o7-af65f7df-e4ef-497f-9cb7-b4545d76045e.png/v1/fill/w_400,h_400/logo_glind_by_coloringdancingedits_dj1p9o7-fullview.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NDAwIiwicGF0aCI6IlwvZlwvMzA0NGY3M2MtMDU0Ny00YjAxLWFlZWMtN2ViZmY2NTU1ZTFiXC9kajFwOW83LWFmNjVmN2RmLWU0ZWYtNDk3Zi05Y2I3LWI0NTQ1ZDc2MDQ1ZS5wbmciLCJ3aWR0aCI6Ijw9NDAwIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.e7HioozPY8w7uJYU9ucOlj32A2t67eokOm5vkh3go-A"
        
        try:
            # Descargar la imagen del logo
            response = requests.get(logo_url)
            response.raise_for_status()  # Verifica si hubo errores en la descarga
            data = BytesIO(response.content)
            core_image = CoreImage(data, ext="png")

            # Crear el widget Image con la imagen descargada y ajustarlo
            self.logo = Image(texture=core_image.texture, size_hint=(None, None), size=(240, 320), pos_hint={'center_x': 0.5, 'center_y': 0.7})
            self.add_widget(self.logo)
        except Exception as e:
            print(f"Error al descargar o cargar el logo: {e}")


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

        self.save_button = Button(
            text="Registrar",
            size_hint=(1, None),
            height=40,
            background_color=(0.6, 0, 0, 1)
        )
        self.save_button.bind(on_release=self.register_data)
        self.add_widget(self.save_button)


        self.log_button = ButtonLogin(
            text="Si ya tienes una cuenta, Inicia Sesión",
            size_hint=(None, None),
            height=40,
            width=200, 
            pos_hint={'center_x': 0.5}  
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