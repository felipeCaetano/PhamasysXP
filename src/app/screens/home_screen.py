from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFloatingActionButton
from kivy.metrics import dp
import os

KV_PATH = os.path.join(os.path.dirname(__file__), "../ui/kv/home_screen.kv")
Builder.load_file(KV_PATH)


class HomeScreen(MDScreen):

    def go_to_cadastrar_clientes(self, *args):
        """Navega para a tela de cadastro de clientes"""
        self.manager.current = "cadastro_cliente"

    def go_to_notas_fiscais(self, *args):
        """Navega para a tela de notas fiscais"""
        self.manager.current = "notas_fiscais"

    def setup_user_level(self, level: str):
        """Define permissões de botões com base no nível do usuário"""
        if level.lower() == "vendedor":
            if hasattr(self.ids, "btn_relatorios"):
                self.ids.btn_relatorios.disabled = True
            if hasattr(self.ids, "btn_estoque"):
                self.ids.btn_estoque.disabled = True
        elif level.lower() == "farmaceutico":
            if hasattr(self.ids, "btn_relatorios"):
                self.ids.btn_relatorios.disabled = True
        # Gerente: acesso total
