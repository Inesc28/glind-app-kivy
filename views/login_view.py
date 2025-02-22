from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from backend.users import validate_user
from views.home_view import HomeView
class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 20
        self.title = Label(
            text="Iniciar Sesión",
            font_size='24sp',
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.title)
        self.username_field = TextInput(
            hint_text="Username",
            multiline=False,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.username_field)
        self.password_field = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.password_field)
        self.save_button = Button(
            text="Iniciar Sesión",
            size_hint=(1, None),
            height=40,
            background_color=(0.6, 0.2, 0.8, 1)
        )
        self.save_button.bind(on_release=self.credentials_access)
        self.add_widget(self.save_button)

    def credentials_access(self, instance):
        user_id = validate_user(self.username_field.text, self.password_field.text)
        if user_id:
            self.handle_login(user_id)
        else:
            popup = Popup(
                title='Error',
                content=Label(text='Usuario o contraseña incorrectos.'),
                size_hint=(None, None),
                size=(400, 400)
            )
            popup.open()

    def handle_login(self, user_id):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(HomeView(logged_in_user_id=user_id))
