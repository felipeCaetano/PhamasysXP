from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast


class CadastroClienteScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "cadastro_cliente"

        # Layout principal da tela
        main_layout = MDBoxLayout(orientation="vertical", padding=10,
                                  spacing=10)

        # Campos de entrada de dados
        self.nome = MDTextField(hint_text="Nome",
                                helper_text="Digite o nome do cliente",
                                helper_text_mode='on_focus',
                                write_tab=False, required=True)
        self.telefone = MDTextField(hint_text="Telefone",
                                    helper_text='(xx) XXXXX-XXXX',
                                    helper_text_mode='on_focus',
                                    write_tab=False, required=True)
        self.email = MDTextField(hint_text="Email",
                                 helper_text='email do cliente',
                                 helper_text_mode='on_focus',
                                 write_tab=False, required=True)
        self.cpf = MDTextField(hint_text="CPF", helper_text='só números',
                               helper_text_mode='on_focus',
                               write_tab=False, required=True)

        # Menu dropdown para seleção de sexo
        self.sexo = MDTextField(hint_text="Sexo", on_focus=self.open_menu)

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

        # Adicionando os campos ao layout principal
        main_layout.add_widget(self.nome)
        main_layout.add_widget(self.telefone)
        main_layout.add_widget(self.email)
        main_layout.add_widget(self.cpf)
        main_layout.add_widget(self.sexo)

        # Botão para cadastrar o cliente
        btn_cadastrar = MDRaisedButton(
            text="Cadastrar Cliente",
            pos_hint={"center_x": 0.5},
            on_release=self.cadastrar_cliente
        )
        main_layout.add_widget(btn_cadastrar)

        # Adiciona o layout principal à tela
        self.add_widget(main_layout)

    def set_sexo(self, sexo):
        self.sexo.text = sexo
        self.sexo_menu.dismiss()

    def open_menu(self, *args):
        if self.sexo.focus:
            self.sexo_menu.open()

    def cadastrar_cliente(self, instance):
        # Captura e valida os dados do cliente
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
        # Limpa os campos após o cadastro
        self.nome.text = self.telefone.text = self.email.text = self.cpf.text = self.sexo.text = ""
