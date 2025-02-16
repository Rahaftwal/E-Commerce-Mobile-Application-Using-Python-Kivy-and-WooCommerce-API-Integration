from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import requests
from requests.auth import HTTPBasicAuth
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
# KivyMD imports
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel

class SignUpScreen(Screen):
    baseUrl = "YOUR_WEBSITE_URL"  # Define the base URL for WooCommerce API
    consumerKey = "YOUR_CONSUMER_KEY"  # Define the consumer key for WooCommerce API
    consumerSecret = "YOUR_CONSUMER_SECRET"  # Define the consumer secret for WooCommerce API

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Back button
        back_button = MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1, "center_y": 0.95},
            on_press=self.go_back
        )
        layout.add_widget(back_button)

        # Title
        title = MDLabel(
            text='Create Account',
            font_style='H4',
            halign='center',
            theme_text_color="Primary",
            size_hint_y=0.2
        )
        layout.add_widget(title)

        # Input fields
        self.first_name_input = MDTextField(
            hint_text='First Name',
            icon_right='account',
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.first_name_input)

        self.last_name_input = MDTextField(
            hint_text='Last Name',
            icon_right='account',
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.last_name_input)

        self.email_input = MDTextField(
            hint_text='Email',
            icon_right='email',
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.email_input)

        self.password_input = MDTextField(
            hint_text='Password',
            icon_right='lock',
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
            password=True
        )
        layout.add_widget(self.password_input)

        self.phone_input = MDTextField(
            hint_text='Phone Number',
            icon_right='phone',
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.phone_input)

        self.city_input = MDTextField(
            hint_text='City',
            icon_right='city',
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.city_input)

        # Sign up button
        btn_sign_up = MDRaisedButton(
            text='Create Account',
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
            on_press=self.sign_up,
            md_bg_color=[0.2, 0.6, 0.9, 1]
        )
        layout.add_widget(btn_sign_up)

        self.add_widget(layout)

    def sign_up(self, instance):
        # Validate inputs
        if not all([
            self.first_name_input.text,
            self.last_name_input.text,
            self.email_input.text,
            self.password_input.text,
            self.phone_input.text,
            self.city_input.text
        ]):
            return

        data = {
            'first_name': self.first_name_input.text,
            'last_name': self.last_name_input.text,
            'email': self.email_input.text,
            'password': self.password_input.text,
            'phone': self.phone_input.text,
            'billing': {
                'city': self.city_input.text
            }
        }

        try:
            response = requests.post(
                f'{self.baseUrl}/wp-json/wc/v3/customers',
                auth=HTTPBasicAuth(self.consumerKey, self.consumerSecret),
                json=data
            )

            if response.status_code == 201:
                data = response.json()
                store = JsonStore('settings.json')
                store.put('user', user_id=data['id'], is_guest=False)
                self.manager.current = 'shop'
            else:
                print(f"Sign up failed: {response.status_code} - {response.text}")

        except requests.RequestException as e:
            print(f"Sign up failed: {str(e)}")

    def go_back(self, instance):
        self.manager.current = 'selection_operation'
