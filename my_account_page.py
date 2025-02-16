from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import requests
from requests.auth import HTTPBasicAuth

from sign_up import SignUpScreen

from kivy.graphics import Color, Rectangle

class MyAccountScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0, 0, 0, 1)  
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.first_name_label = Label(text='First Name: ', font_size=24, size_hint_y=0.2, color=(1, 1, 1, 1))
        layout.add_widget(self.first_name_label)

        self.last_name_label = Label(text='Last Name: ', font_size=24, size_hint_y=0.2, color=(1, 1, 1, 1))
        layout.add_widget(self.last_name_label)

        self.username_label = Label(text='Username: ', font_size=24, size_hint_y=0.2, color=(1, 1, 1, 1))
        layout.add_widget(self.username_label)

        self.email_label = Label(text='Email: ', font_size=24, size_hint_y=0.2, color=(1, 1, 1, 1))
        layout.add_widget(self.email_label)

        self.phone_label = Label(text='Phone: ', font_size=24, size_hint_y=0.2, color=(1, 1, 1, 1))
        layout.add_widget(self.phone_label)

        self.city_label = Label(text='City: ', font_size=24, size_hint_y=0.2, color=(1, 1, 1, 1))
        layout.add_widget(self.city_label)

        btn_log_out = Button(text='Log Out', size_hint_y=0.2)
        btn_log_out.bind(on_press=self.log_out)
        layout.add_widget(btn_log_out)

        self.add_widget(layout)
        self.update_account_info()

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_account_info(self):
        store = JsonStore('settings.json')
        user_id = store.get('user')['user_id']

        url = 'YOUR_WEBSITE_URL/wp-json/wc/v3/customers/{user_id}'
        try:
            response = requests.get(url, auth=HTTPBasicAuth(SignUpScreen.consumerKey, SignUpScreen.consumerSecret))
            if response.status_code == 200:
                user_data = response.json()
                self.first_name_label.text = f'First Name: {user_data.get("first_name", "Unknown")}'
                self.last_name_label.text = f'Last Name: {user_data.get("last_name", "Unknown")}'
                self.username_label.text = f'Username: {user_data.get("username", "Unknown")}'
                self.email_label.text = f'Email: {user_data.get("email", "Unknown")}'
                self.phone_label.text = f'Phone: {user_data.get("phone", "Unknown")}'
                self.city_label.text = f'City: {user_data.get("billing", {}).get("city", "Unknown")}'
            else:
                self.first_name_label.text = 'Failed to retrieve information'
                self.last_name_label.text = ''
                self.username_label.text = ''
                self.email_label.text = ''
                self.phone_label.text = ''
                self.city_label.text = ''

        except requests.RequestException as e:
            self.first_name_label.text = f'Failed to retrieve information: {str(e)}'
            self.last_name_label.text = ''
            self.username_label.text = ''
            self.email_label.text = ''
            self.phone_label.text = ''
            self.city_label.text = ''

    def log_out(self, instance):
        store = JsonStore('settings.json')
        store.put('user', user_id=None, is_guest=True)
        self.manager.current = 'selection_operation'
