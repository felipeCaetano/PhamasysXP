from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'Login_Screen'
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        header_image = Image(
            source="assets/pharmasys_logo.png",
            size_hint=(1, 1),
            allow_stretch=True
        )
        layout.add_widget(header_image)
        # Texto de boas-vindas
        welcome_label = MDLabel(
            text="Faça o Login",
            halign="center",
            theme_text_color="Primary",
            font_style="H5"
        )
        layout.add_widget(welcome_label)

        # Campo de email
        self.user_login = MDTextField(
            hint_text="login",
            icon_right="login-variant",
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
            write_tab=False
        )
        layout.add_widget(self.user_login)

        # Campo de senha
        self.password = MDTextField(
            hint_text="Password",
            icon_right="lock-outline",
            password=True,
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
            write_tab=False
        )
        layout.add_widget(self.password)

        # Botão de Login
        login_button = MDRaisedButton(
            text="Log In",
            size_hint=(0.8, None),
            height=48,
            pos_hint={"center_x": 0.5},
            on_release=self.login
        )
        layout.add_widget(login_button)

        # Adicionando o layout à tela
        self.add_widget(layout)

    def login(self, instance):
        # Exemplo: credenciais hardcoded e níveis
        credentials = {
            "vendedor": {"password": "senha123", "level": "Vendedor"},
            "farmaceutico": {"password": "senha456", "level": "Farmacêutico"},
            "gerente": {"password": "senha789", "level": "Gerente"},
        }

        user = self.user_login.text
        passwd = self.password.text

        if user in credentials and credentials[user]["password"] == passwd:
            level = credentials[user]["level"]
            toast(f"Bem-vindo, {level}!")
            self.manager.get_screen("home").setup_user_level(level)
            self.manager.current = "home"
        else:
            toast("Usuário ou senha incorretos")
