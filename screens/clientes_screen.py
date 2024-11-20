from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar

from custom_items.menu_icon_tooltip_bar import MenuIconToolTipBar

# Primeiro carrega o componente TooltipMDIconButton
Builder.load_file('custom_items/tooltip_icon_button.kv')
# Depois carrega o MenuIconToolTipBar
Builder.load_file('custom_items/menu_icon_tooltip_bar.kv')


class CadastroClienteScreen(MDScreen):
    def __init__(self, **kwargs):
        app = MDApp.get_running_app()
        super().__init__(**kwargs)
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=0
        )
        appbar = MDTopAppBar(
        title="Cadastro de Clientes",
        left_action_items=[["arrow-left", lambda x: app.voltar_tela_principal()]],
        right_action_items=[["menu", lambda x: self.clear_fields()]]
        )
        # self.add_widget(appbar)
        tooltipbar = MenuIconToolTipBar(
            size_hint_y=None, height="48dp",
            import_icon='file-account',
            import_tooltip="Importar Cliente",
            save_icon="content-save-outline",
            save_tooltip="Salvar Cliente",
            show_filter=False,
            show_view=False
        )
        tooltipbar.bind(on_import_press=self.importar_dados,
                        on_clear_press=self.limpar_campos,
                        on_save_press=self.salvar_dados,
                        )
        content_layout = MDBoxLayout(
            adaptive_height=True,
            orientation="vertical",
            padding=20,
            spacing=10,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.card = MDCard(
            orientation="vertical",
            size_hint=(0.9, None),
            height="450dp",
            padding=20,
            elevation=6,
            style="elevated",
            shadow_softness=10,
            shadow_offset=(3, 3),
            pos_hint = {"center_x": 0.5, "center_y": 0.5},
        )

        self.nome = MDTextField(hint_text="Nome",
                                helper_text="Digite o nome do cliente",
                                helper_text_mode='on_focus',
                                write_tab=False, icon_right="account",
                                required=True)
        self.telefone = MDTextField(hint_text="Telefone",
                                    helper_text='(0xx) XXXXX-XXXX',
                                    phone_mask="(###) ###-####",
                                    helper_text_mode='on_focus',
                                    write_tab=False,  icon_right="phone",
                                    required=True)
        self.email = MDTextField(hint_text="Email",
                                 helper_text='email do cliente',
                                 helper_text_mode='on_focus',
                                 write_tab=False, icon_right="email",
                                 required=True)
        self.cpf = MDTextField(hint_text="CPF", helper_text='só números',
                               helper_text_mode='on_focus',
                               write_tab=False,
                               icon_right="card-account-details",
                               required=True)
        self.sexo = MDTextField(hint_text="Sexo",
                                icon_right="gender-male-female",
                                on_focus=self.open_menu)

        self.menu_items = [
            {"text": "Masculino",
             "on_release": lambda x="Masculino": self.set_sexo(x)},
            {"text": "Feminino",
             "on_release": lambda x="Feminino": self.set_sexo(x)},
            {"text": "Outro",
             "on_release": lambda x="Outro": self.set_sexo(x)},
        ]
        self.sexo_menu = MDDropdownMenu(caller=self.sexo,
                                        items=self.menu_items, width_mult=4)
        self.sexo_menu.bind(on_release=self.set_sexo)
        self.sexo.bind(focus=self.open_menu)
        self.card.add_widget(self.nome)
        self.card.add_widget(self.telefone)
        self.card.add_widget(self.email)
        self.card.add_widget(self.cpf)
        self.card.add_widget(self.sexo)
        btn_cadastrar = MDRaisedButton(
            text="Cadastrar Cliente",
            pos_hint={"center_x": 0.5},
            on_release=self.cadastrar_cliente
        )
        self.card.add_widget(btn_cadastrar)
        content_layout.add_widget(self.card)
        main_layout.add_widget(appbar)
        main_layout.add_widget(tooltipbar)
        main_layout.add_widget(content_layout)

        # Adiciona o layout principal à tela
        self.add_widget(main_layout)

    def importar_dados(self, *args):
        print("Importando dados...")

    def limpar_campos(self, *args):
        print("Limpando campos...")

    def salvar_dados(self, *args):
        print('salvando no banco')

    def set_sexo(self, sexo):
        self.sexo.text = sexo
        self.sexo_menu.dismiss()

    def open_menu(self, *args):
        if self.sexo.focus:
            self.sexo_menu.open()

    def cadastrar_cliente(self, instance):
        """ Captura e valida os dados do cliente"""
        if not all([self.nome.text, self.telefone.text, self.email.text,
                    self.cpf.text, self.sexo.text]):
            toast("Preencha todos os campos obrigatórios")
            return
        cliente_data = {
            "nome": self.nome.text,
            "telefone": self.telefone.text,
            "email": self.email.text,
            "cpf": self.cpf.text,
            "sexo": self.sexo.text
        }
        # Aqui seria possível adicionar lógica para salvar o cliente no banco de dados
        print("Cliente cadastrado:", cliente_data)
        toast("Cliente cadastrado com sucesso!")
        self.clear_fields()

    def clear_fields(self):
        self.nome.text = self.telefone.text = self.email.text = self.cpf.text = self.sexo.text = ""

