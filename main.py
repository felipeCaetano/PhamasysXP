from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

from screens.clientes_screen import CadastroClienteScreen
from screens.notas_fiscais_screen import NotasFiscaisScreen

KV = '''
MDBoxLayout:
    id: 'layout'
    orientation: 'vertical'
    MDTopAppBar:
        title: "PharmaSys"
        left_action_items: [["menu", lambda x: app.callback()]]
        right_action_items: [["dots-vertical", lambda x: app.callback()]]

    MDLabel:
        text: "Bem-vindo ao sistema de gerenciamento de farmácia!"
        halign: "center"
        size_hint_y: None
        height: self.texture_size[1] + dp(20)
        padding_y: dp(10)
    
    Widget:
'''


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'

        # Carrega o layout definido pela string KV
        layout = Builder.load_string(KV)
        self.add_widget(layout)  # Adiciona o layout à tela

        # Exemplo de botão que leva à tela de notas fiscais
        button = MDFloatingActionButton(
            icon="file-document",
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            on_release=self.go_to_notas_fiscais
        )
        self.add_widget(button)

        button_cadastro_cliente = MDFloatingActionButton(
            icon="account-plus",
            pos_hint={"center_x": 0.6, "center_y": 0.1},
            on_release=self.go_to_cadastrar_clientes
        )
        self.add_widget(button_cadastro_cliente)

    def go_to_cadastrar_clientes(self, *args):
        self.manager.current = 'cadastro_cliente'

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
        sm.add_widget(CadastroClienteScreen())
        return sm

    def navigation_drawer(self):
        pass  # Aqui você pode adicionar a lógica para abrir um menu lateral.

    def callback(self):
        pass


if __name__ == '__main__':
    PharmaSysApp().run()
