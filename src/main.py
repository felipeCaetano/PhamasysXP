from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.screenmanager import MDScreenManager

from app.screens.home_screen import HomeScreen
from app.screens.login_screen import LoginScreen
from app.screens.notas_fiscais_screen import NotasFiscaisScreen
from app.screens.cadastro_cliente_screen import CadastroClienteScreen
from app.screens.presplash_screen import PreSplash


class PharmaSysApp(MDApp):
    """Aplicativo principal PharmaSys"""

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.sm = MDScreenManager()

        # Adiciona telas ao ScreenManager
        self.sm.add_widget(PreSplash(name="presplash"))
        self.sm.add_widget(LoginScreen(name="login_screen"))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(NotasFiscaisScreen(name="notas_fiscais"))
        self.sm.add_widget(CadastroClienteScreen(name="cadastro_cliente"))

        return self.sm

    def on_start(self):
        # Exemplo: delay para transição do presplash
        Clock.schedule_once(self.show_login, 5)

    def show_login(self, *args):
        """Exibe tela de login"""
        self.sm.current = "login_screen"

    def open_nav_drawer(self, *args):
        """Abre a Navigation Drawer (caso exista)"""
        if hasattr(self.root, "ids") and "nav_drawer" in self.root.ids:
            self.root.ids.nav_drawer.set_state("open")

    def show_options(self, *args):
        """Placeholder para opções do app"""
        print("Opções do app abertas")

    def switch_screen(self, instance_navigation_rail, instance_navigation_rail_item):
        """Troca a tela do MDScreenManager interno da HomeScreen"""
        screen_name = instance_navigation_rail_item.name
        print(f"Switching to screen: {screen_name}")
        home_screen = self.sm.get_screen("home")
        if hasattr(home_screen.ids, "screen_manager_content"):
            home_screen.ids.screen_manager_content.current = screen_name


if __name__ == "__main__":
    PharmaSysApp().run()
