from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

from screens.notas_fiscais_screen import NotasFiscaisScreen

KV = '''
MDBoxLayout:
    orientation: 'vertical'
    MDTopAppBar:
        title: "PharmaSys"
        left_action_items: [["menu", lambda x: app.callback()]]
        right_action_items: [["dots-vertical", lambda x: app.callback()]]

    MDLabel:
        text: "Bem-vindo ao sistema de gerenciamento de farmácia!"
        halign: "center"
'''


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'

        # Exemplo de botão que leva à tela de notas fiscais
        button = MDFloatingActionButton(
            icon="file-document",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.go_to_notas_fiscais
        )
        self.add_widget(button)

    def go_to_notas_fiscais(self, *args):
        # Acessa o gerenciador de telas e muda para 'notas_fiscais'
        self.manager.current = 'notas_fiscais'


class PharmaSysApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        # Instancia o ScreenManager
        sm = MDScreenManager()

        # Adiciona a tela principal (home) e a de notas fiscais
        sm.add_widget(HomeScreen())
        sm.add_widget(NotasFiscaisScreen())

        return sm

    def navigation_drawer(self):
        pass  # Aqui você pode adicionar a lógica para abrir um menu lateral.

    def callback(self):
        pass


if __name__ == '__main__':
    PharmaSysApp().run()
