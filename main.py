from kivymd.app import MDApp
from kivy.lang import Builder

KV = '''
MDBoxLayout:
    orientation: 'vertical'
    MDTopAppBar:
        title: "MDTopAppBar"

    MDLabel:
        text: "Bem-vindo ao sistema de gerenciamento de farmácia!"
        halign: "center"
'''


class FarmaciaApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def navigation_drawer(self):
        pass  # Aqui você pode adicionar a lógica para abrir um menu lateral.


if __name__ == '__main__':
    FarmaciaApp().run()
