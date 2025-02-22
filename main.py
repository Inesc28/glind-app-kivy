from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from views.register import RegisterScreen

class MainApp(App):
    def build(self):
        self.title = "Glind"
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(RegisterScreen())
        return layout

if __name__ == "__main__":
    MainApp().run()
