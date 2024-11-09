from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer, \
    MDNavigationDrawerMenu, MDNavigationDrawerItem
from kivymd.uix.navigationrail import MDNavigationRail, \
    MDNavigationRailMenuButton, MDNavigationRailFabButton, MDNavigationRailItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

from screens.clientes_screen import CadastroClienteScreen
from screens.login_screen import LoginScreen
from screens.notas_fiscais_screen import NotasFiscaisScreen
from screens.presplash_screen import PreSplash

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

    def setup_user_level(self, level):
        # Exemplo de controle de acesso com base no nível
        if level == "Vendedor":
            self.btn_relatorios.disabled = True
            self.btn_estoque.disabled = True
        elif level == "Farmacêutico":
            self.btn_relatorios.disabled = True
        # Gerente tem acesso total


class PharmaSysApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.sm = MDScreenManager()
        # # Instancia o ScreenManager
        # sm = MDScreenManager()
        # Adiciona a tela principal (home) e a de notas fiscais
        self.sm.add_widget(PreSplash())
        self.sm.add_widget(LoginScreen())
        self.screen = HomeScreen(name='home')
        self.sm.add_widget(self.screen)
        self.sm.add_widget(NotasFiscaisScreen())
        self.sm.add_widget(CadastroClienteScreen())
        return self.sm

    def on_start(self):
        Clock.schedule_once(self.callback, 5)

    def open_nav_drawer(self, *args):
        self.root.ids.nav_drawer.set_state("open")

    def callback(self, *args):
        self.root.current = 'Login_Screen'

    def switch_screen(self, instance_navigation_rail,
                      instance_navigation_rail_item):
        """Troca a tela do MDScreenManager interno da HomeScreen."""
        screen_name = instance_navigation_rail_item.name
        print(screen_name)
        screen_manager_content = self.root.get_screen(
            'home').ids.screen_manager_content
        screen_manager_content.current = screen_name


if __name__ == '__main__':
    PharmaSysApp().run()
