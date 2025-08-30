from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder

KV = '''
<VendorCard>:
    orientation: "vertical"
    size_hint: (1, None)
    height: "100dp"
    padding: "8dp"
    spacing: "8dp"
    md_bg_color: app.theme_cls.accent_light

    MDBoxLayout:
        orientation: "horizontal"
        padding: "10dp"
        spacing: "4dp"

        MDTextField:
            text: root.nome
            theme_text_color: "Secondary"
            hint_text: "Nome:"
           
        MDTextField:
            text: root.cnpj
            theme_text_color: "Hint"
            hint_text: "CNPJ:"

        MDTextField:
            text: root.nome_fantasia
            theme_text_color: "Hint"
            hint_text: "Nome Fantasia:"
        
        MDTextField:
            text: root.telefone
            theme_text_color: "Hint"
            hint_text: "Telefone:"
            
        MDTextField:
            theme_text_color: "Hint"
            hint_text: "Email:"
            
        MDIconButton:
            id: cadastrar_fornecedor
            icon: "check"
            pos_hint: {"center_x": 0.9, "center_y": 0.1}
            on_release: root.cadastrar_fornecedor(self)
'''

Builder.load_string(KV)


class VendorCard(MDCard):
    nome = StringProperty()
    cnpj = StringProperty()
    nome_fantasia = StringProperty()
    telefone = StringProperty()
    cadastrar_fornecedor = ObjectProperty()
