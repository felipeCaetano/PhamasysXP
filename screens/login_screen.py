from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'Login_Screen'
        lbl_hello = MDLabel(text="PharmaSys")
        self.add_widget(lbl_hello)
