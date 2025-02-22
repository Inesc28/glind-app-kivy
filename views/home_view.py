import requests
from io import BytesIO
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton
from backend.users import connect_to_server_threaded, get_user_data, get_connected_users

class HomeView(BoxLayout):
    def __init__(self, logged_in_user_id, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.logged_in_user_id = logged_in_user_id
        connect_to_server_threaded(logged_in_user_id, self)
        self.create_ui()

    def create_ui(self):
        user_info = get_user_data(self.logged_in_user_id)
        
        if user_info:
            user_code = Label(text=f"ID: {user_info['id']}")
            user_name = Label(text=f"Usuario: {user_info['user']}")
        else:
            user_code = Label(text="ID desconocido")
            user_name = Label(text="Usuario desconocido")
        
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
        
        # ActionBar como AppBar
        self.appbar = ActionBar(pos_hint={'top': 1})
        self.action_view = ActionView()
        
        self.action_previous = ActionPrevious(with_previous=False, title='Glind')
        self.action_view.add_widget(self.action_previous)
        
        self.settings_button = ActionButton(text='Settings', on_release=lambda x: print("Abrir configuraciones..."))
        self.action_view.add_widget(self.settings_button)
        
        self.appbar.add_widget(self.action_view)
        
        self.refresh_button = Button(text="Actualizar Lista", on_press=self.refresh_ui)
        
        self.add_widget(self.appbar)
        self.add_widget(user_name)
        self.add_widget(user_code)
        self.add_widget(self.refresh_button)
        
        self.connected_users_list = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.connected_users_list)
        
        self.refresh_ui()

    def refresh_ui(self, *args):
        self.connected_users_list.clear_widgets()
        connected_users = get_connected_users(self.logged_in_user_id)
        if connected_users:
            for user in connected_users:
                user_id = user.get("userId")
                username = user.get("username")
                if user_id != self.logged_in_user_id:
                    user_label = Label(text=f"Usuario: {username}")
                    user_button = Button(text="Visualizar pantalla", size_hint=(None, None), size=(150, 40))
                    user_button.bind(on_press=lambda x, user_id=user_id: self.visualizar(user_id))
                    user_layout = BoxLayout(orientation='horizontal')
                    user_layout.add_widget(user_label)
                    user_layout.add_widget(user_button)
                    self.connected_users_list.add_widget(user_layout)

    def visualizar(self, user_id):
        print(f"Visualizando pantalla del usuario {user_id}.")
