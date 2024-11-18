from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

from screens.nfe_import import NFEScreen

# Definindo o estilo das telas em KV Language
KV = '''
<SplashScreen>:
    MDBoxLayout:
        md_bg_color: 0, 10/255, 226/255
        orientation: 'vertical'
        spacing: '20dp'
        padding: '20dp'
        MDLabel:
            text: 'PharmaSys'
            halign: 'center'
            font_style: 'H2'
            theme_text_color: "Secondary"
        MDSpinner:
            size_hint: None, None
            size: dp(46), dp(46)
            pos_hint: {'center_x': .5}
            active: True

<LoginScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: '20dp'
        padding: '20dp'

        MDLabel:
            text: 'PharmaSys'
            halign: 'center'
            font_style: 'H4'
            theme_text_color: "Primary"

        MDTextField:
            id: username
            hint_text: "Nome de usuário"
            icon_right: "account"
            helper_text: "Digite seu nome de usuário"
            helper_text_mode: "on_error"
            pos_hint: {'center_x': .5}
            size_hint_x: .8
            write_tab: False

        MDTextField:
            id: password
            hint_text: "Senha"
            icon_right: "eye-off"
            helper_text: "Digite sua senha"
            helper_text_mode: "on_error"
            password: True
            pos_hint: {'center_x': .5}
            size_hint_x: .8
            write_tab: False

        Spinner:
            id: user_type
            text: 'Selecione o tipo de usuário'
            values: ['Vendedor', 'Farmacêutico', 'Gerente']
            size_hint: None, None
            size: dp(200), dp(50)
            pos_hint: {'center_x': .5}

        MDRaisedButton:
            text: "Entrar"
            pos_hint: {'center_x': .5}
            on_release: app.verify_login(username.text, password.text, user_type.text)

<MenuCard>:
    orientation: 'vertical'
    padding: "8dp"
    size_hint: None, None
    size: "180dp", "180dp"
    pos_hint: {"center_x": .5, "center_y": .5}

    MDIconButton:
        icon: root.icon
        pos_hint: {"center_x": .5}
        icon_size: "64dp"
        theme_icon_color: "Custom"
        icon_color: app.theme_cls.primary_color
        on_release: root.on_press()

    MDLabel:
        text: root.text
        halign: "center"
        theme_text_color: "Primary"

<MainScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: '10dp'

        MDTopAppBar:
            title: "PharmaSys"
            left_action_items: [["menu", lambda x: app.toggle_nav_drawer()]]
            right_action_items: [["logout", lambda x: app.logout()]]

        MDLabel:
            id: welcome_label
            text: "Bem-vindo!"
            halign: "center"
            font_style: "H5"
            size_hint_y: None
            height: self.texture_size[1]

        MDGridLayout:
            cols: 3
            padding: "20dp"
            spacing: "20dp"

            MenuCard:
                icon: "cash-register"
                text: "Vendas"
                on_press: app.handle_menu_click("vendas")
            
            MenuCard:
                icon: "file-document"
                text: "Notas Fiscais"
                on_press: app.handle_menu_click("nfe")

            MenuCard:
                icon: "pill"
                text: "Medicamentos"
                on_press: app.handle_menu_click("medicamentos")

            MenuCard:
                icon: "account-group"
                text: "Clientes"
                on_press: app.handle_menu_click("clientes")

            MenuCard:
                icon: "chart-line"
                text: "Relatórios"
                on_press: app.handle_menu_click("relatorios")
'''


class MenuCard(MDCard):
    icon = StringProperty()
    text = StringProperty()
    def on_press(self):
        pass


class SplashScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class PharmaSysApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None
        self.current_user_type = None


    def load_all_screens(self):
        self.screens = {
            'splash': SplashScreen(name='splash'),
            'login': LoginScreen(name='login'),
            'main': MainScreen(name='main'),
            'nfe': NFEScreen(name='nfe')
        }

    def build(self):
        # Carrega o estilo KV
        Builder.load_string(KV)
        self.load_all_screens()
        # Configura o gerenciador de telas
        self.sm = ScreenManager(transition=FadeTransition())
        # Adiciona todas as telas ao gerenciador
        for screen in self.screens.values():
            self.sm.add_widget(screen)

        # Configura o tema do app
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        # Agenda a transição da tela de splash
        Clock.schedule_once(self.switch_to_login, 5)

        return self.sm

    def switch_to_login(self, dt):
        self.sm.current = 'login'

    def verify_login(self, username, password, user_type):
        if not username or not password:
            self.show_dialog("Erro", "Por favor, preencha todos os campos.")
            return

        if user_type == 'Selecione o tipo de usuário':
            self.show_dialog("Erro", "Por favor, selecione um tipo de usuário.")
            return

        # Exemplo de credenciais (em produção, use um banco de dados e hash das senhas)
        credentials = {
            'Vendedor': {'user': 'vendedor', 'pass': '123',
                         'permissions': ['vendas', 'clientes']},
            'Farmacêutico': {'user': 'farmaceutico', 'pass': '456',
                             'permissions': ['medicamentos', 'vendas',
                                             'clientes', 'nfe']},
            'Gerente': {'user': 'gerente', 'pass': '789',
                        'permissions': ['vendas', 'medicamentos', 'clientes',
                                        'relatorios', 'nfe']}
        }

        if (user_type in credentials and
                username == credentials[user_type]['user'] and
                password == credentials[user_type]['pass']):

            self.current_user = username
            self.current_user_type = user_type
            self.user_permissions = credentials[user_type]['permissions']

            # Atualiza o texto de boas-vindas
            main_screen = self.sm.get_screen('main')
            welcome_label = main_screen.ids.welcome_label
            welcome_label.text = f"Bem-vindo, {username} ({user_type})"

            # Muda para a tela principal
            self.sm.current = 'main'
        else:
            self.show_dialog("Erro", "Credenciais inválidas.")

    def handle_menu_click(self, menu_item):
        if menu_item not in self.user_permissions:
            self.show_dialog("Acesso Negado",
                             "Você não tem permissão para acessar esta funcionalidade.")
            return

        # Aqui você implementaria a navegação para cada funcionalidade
        actions = {
            'vendas': self.show_vendas,
            'medicamentos': self.show_medicamentos,
            'clientes': self.show_clientes,
            'relatorios': self.show_relatorios,
            'nfe': self.show_notas
        }

        if menu_item in actions:
            actions[menu_item]()

    def show_vendas(self):
        self.show_dialog("Vendas", "Módulo de vendas em desenvolvimento.")

    def show_medicamentos(self):
        self.show_dialog("Medicamentos",
                         "Módulo de medicamentos em desenvolvimento.")

    def show_clientes(self):
        self.show_dialog("Clientes", "Módulo de clientes em desenvolvimento.")

    def show_relatorios(self):
        self.show_dialog("Relatórios",
                         "Módulo de relatórios em desenvolvimento.")
    def show_notas(self):
        self.sm.current = 'nfe'

    def logout(self):
        self.current_user = None
        self.current_user_type = None
        self.user_permissions = []
        self.sm.current = 'login'

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def toggle_nav_drawer(self, *args):
        pass

    def voltar_tela_principal(self, *args):
        self.sm.current = 'main'


if __name__ == '__main__':
    PharmaSysApp().run()