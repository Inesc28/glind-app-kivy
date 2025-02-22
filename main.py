import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from views.register import RegisterScreen
from kivy.core.image import Image as CoreImage
from io import BytesIO

class MainApp(App):
    def build(self):
        self.title = "Glind"
        layout = FloatLayout()

        url = 'https://img.freepik.com/premium-photo/abstract-black-background-copy-space_1019279-207.jpg'
        
        try:
            response = requests.get(url)
            response.raise_for_status()  
            data = BytesIO(response.content)
            core_image = CoreImage(data, ext="png")

            background_image = Image(texture=core_image.texture, allow_stretch=True, keep_ratio=False)
            layout.add_widget(background_image)
        except Exception as e:
            print(f"Error al descargar o cargar la imagen de fondo: {e}")

        components_layout = BoxLayout(orientation='vertical')
        components_layout.add_widget(RegisterScreen())
        
        layout.add_widget(components_layout)

        return layout

if __name__ == "__main__":
    MainApp().run()
