from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp 
# KivyMD imports
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
class SelectionOperationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create main layout
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        # Set white background
        with layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

        # App title with attractive design
        title = MDLabel(
            text='Welcome',
            font_style='H4',
            halign='center',
            theme_text_color="Primary",
            size_hint_y=0.2
        )
        layout.add_widget(title)

        subtitle = MDLabel(
            text='Choose your login method',
            font_style='Subtitle1',
            halign='center',
            theme_text_color="Secondary",
            size_hint_y=0.1
        )
        layout.add_widget(subtitle)

        # Create cards for buttons
        buttons_layout = BoxLayout(orientation='vertical', spacing=dp(15))

        # Sign In card
        signin_card = self._create_action_card(
            'Sign In',
            'Access your existing account',
            'account',
            self.sign_in
        )
        buttons_layout.add_widget(signin_card)

        # Sign Up card
        signup_card = self._create_action_card(
            'Sign Up',
            'Create a new account',
            'account-plus',
            self.sign_up
        )
        buttons_layout.add_widget(signup_card)

        # Guest card
        guest_card = self._create_action_card(
            'Browse as Guest',
            'Explore without registration',
            'account-arrow-right',
            self.browse_as_guest
        )
        buttons_layout.add_widget(guest_card)

        layout.add_widget(buttons_layout)
        self.add_widget(layout)

    def _create_action_card(self, title, subtitle, icon, on_press_callback):
        card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(100),
            padding=dp(15),
            elevation=2,
            radius=[dp(10)]
        )

        content = BoxLayout(orientation='horizontal')
        
        icon_widget = MDIconButton(
            icon=icon,
            theme_text_color="Primary",
            size_hint_x=0.2
        )
        
        text_layout = BoxLayout(orientation='vertical', size_hint_x=0.8)
        title_label = MDLabel(
            text=title,
            theme_text_color="Primary",
            font_style='H6'
        )
        subtitle_label = MDLabel(
            text=subtitle,
            theme_text_color="Secondary",
            font_style='Caption'
        )
        
        text_layout.add_widget(title_label)
        text_layout.add_widget(subtitle_label)
        
        content.add_widget(icon_widget)
        content.add_widget(text_layout)
        card.add_widget(content)
        
        card.bind(on_release=on_press_callback)
        return card

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def sign_in(self, instance):
        self.manager.current = 'sign_in'

    def sign_up(self, instance):
        self.manager.current = 'sign_up'

    def browse_as_guest(self, instance):
        store = JsonStore('settings.json')
        store.put('user', user_id=None, is_guest=True)
        self.manager.current = 'shop'
