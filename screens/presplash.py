from kivy.metrics import sp
from kivy.uix.image import Image
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class PreSplash(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'pre-splash'
        layout = MDFloatLayout(
            md_bg_color=(0, 48/255, 226/255)
        )
        logo = Image(
            source="assets/pharmasyssplash.jpg",
            size_hint=(.26, .26),
            pos_hint={'center_x': .5, 'center_y': .55},
        )
        layout.add_widget(logo)
        developed = MDLabel(
            text="Desenvolvido por MHC Systems",
            pos_hint={'center_x': .5, 'center_y': .2},
            halign='center',
            font_size=sp(35)
        )
        layout.add_widget(developed)
        slogan = MDLabel(
            text="Conectando Ideias ao Futuro.",
            pos_hint={'center_x': .5, 'center_y': .15},
            halign='center',
            font_size=sp(20)
        )
        self.add_widget(layout)

