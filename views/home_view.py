from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.app import App

from backend.users import connect_to_server_threaded, get_user_data, get_connected_users

class UserListView(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []

class HomeScreen(BoxLayout):

    def __init__(self, logged_in_user_id, **kwargs):
        super().__init__(**kwargs)
        self.logged_in_user_id = logged_in_user_id
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 20

        connect_to_server_threaded(logged_in_user_id, self)

        self.refresh_ui()

    def refresh_ui(self, instance=None):
        self.clear_widgets()

        user_info = get_user_data(self.logged_in_user_id)

        if user_info:
            user_code = Label(text=f"ID: {user_info['id']}")
            user_name = Label(text=f"Usuario: {user_info['user']}")
        else:
            user_code = Label(text="ID desconocido")
            user_name = Label(text="Usuario desconocido")

        self.add_widget(user_code)
        self.add_widget(user_name)

        refresh_button = Button(
            text="Actualizar Lista",
            size_hint=(1, None),
            height=40,
            background_color=(0.6, 0.2, 0.8, 1),
            on_release=self.refresh_ui
        )
        self.add_widget(refresh_button)

        connected_users_list = get_connected_users(self.logged_in_user_id)
        user_list_view = UserListView()
        user_list_view.data = [{'text': user['username']} for user in connected_users_list]

        self.add_widget(user_list_view)

    def desvincular(self, user_id):
        print(f"Usuario {user_id} desvinculado.")
        # Lógica para desvincular al usuario

    def visualizar(self, user_id):
        print(f"Visualizando pantalla del usuario {user_id}.")
        # Lógica para visualizar la pantalla del usuario

class MyApp(App):

    def build(self):
        return HomeScreen(logged_in_user_id="user_id")


if __name__ == "__main__":
    MyApp().run()
