from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
import requests
from requests.auth import HTTPBasicAuth
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.graphics import Color, Rectangle

class SignInScreen(Screen):
    baseUrl = "YOUR_WEBSITE_URL"
    consumerKey = "YOUR_CONSUMER_KEY"  # Define the consumer key for WooCommerce API
    consumerSecret = "YOUR_CONSUMER_SECRET"  # Define the consumer secret for WooCommerce API

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main container with white background
        main_layout = BoxLayout(orientation='vertical')
        
        # Set white background
        with main_layout.canvas.before:
            Color(1, 1, 1, 1)  # White background
            Rectangle(pos=main_layout.pos, size=main_layout.size)
        
        # Content layout with padding
        layout = BoxLayout(
            orientation='vertical', 
            padding=dp(20), 
            spacing=dp(20),
            size_hint=(1, 0.95)
        )

        # Back button
        back_button = MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1, "center_y": 0.5},
            on_press=self.go_back,
            theme_text_color="Custom",
            text_color=[0, 0, 0, 1]
        )
        layout.add_widget(back_button)

        # Welcome text
        welcome_text = MDLabel(
            text='Welcome Back!',
            font_style='H4',
            halign='center',
            theme_text_color="Custom",
            text_color=[0, 0, 0, 1],
            size_hint_y=0.15
        )
        layout.add_widget(welcome_text)

        # Subtitle
        subtitle = MDLabel(
            text='Sign in to continue',
            font_style='Subtitle1',
            halign='center',
            theme_text_color="Secondary",
            size_hint_y=0.1
        )
        layout.add_widget(subtitle)

        # Card for input fields
        card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(250),
            padding=dp(20),
            spacing=dp(20),
            elevation=2,
            radius=[dp(10)]
        )

        # Input fields
        self.email_input = MDTextField(
            hint_text='Email',
            icon_right='email',
            size_hint_x=1,
            mode="rectangle",
            helper_text="Enter your email address",
            helper_text_mode="on_error"
        )
        card.add_widget(self.email_input)

        self.password_input = MDTextField(
            hint_text='Password',
            icon_right='lock',
            size_hint_x=1,
            password=True,
            mode="rectangle",
            helper_text="Enter your password",
            helper_text_mode="on_error"
        )
        card.add_widget(self.password_input)

        # Sign in button
        btn_sign_in = MDRaisedButton(
            text='SIGN IN',
            size_hint_x=1,
            height=dp(50),
            md_bg_color=[0.2, 0.6, 0.9, 1],
            on_press=self.sign_in,
            font_size=16
        )
        card.add_widget(btn_sign_in)

        layout.add_widget(card)

        # Add the main layout
        main_layout.add_widget(layout)
        self.add_widget(main_layout)

    def sign_in(self, instance):
        email = self.email_input.text
        password = self.password_input.text

        if not email:
            self.email_input.error = True
            return
        if not password:
            self.password_input.error = True
            return

        url = f'{self.baseUrl}/wp-json/wc/v3/customers'
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.get(
                url, 
                auth=HTTPBasicAuth(self.consumerKey, self.consumerSecret),
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                user = next((user for user in data if user.get('email') == email), None)
                if user:
                    store = JsonStore('settings.json')
                    store.put('user', user_id=user['id'], is_guest=False)
                    self.manager.current = 'shop'
                else:
                    self.email_input.error = True
                    self.email_input.helper_text = "Invalid email or password"
            else:
                print(f"Sign in failed: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print(f"Sign in failed: {str(e)}")

    def go_back(self, instance):
        self.manager.current = 'selection_operation'
