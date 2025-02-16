import json
from kivy.uix.screenmanager import Screen
from kivy.graphics import Rectangle, Color
from kivymd.uix.button import MDIconButton
from kivy.metrics import dp

# Assuming 'wishlist' is imported or defined somewhere
from product_details_page import wishlist

class WishlistPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.update_wishlist()

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_wishlist(self):
        self.ids.items_layout.clear_widgets()
        self.ids.title_label.text = 'Wishlist'  # Set title label text

        for item in wishlist:
            # Create a card-like layout for each item
            card_layout = self._create_card_layout(item)
            self.ids.items_layout.add_widget(card_layout)

    def _create_card_layout(self, item):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.image import AsyncImage

        card_layout = BoxLayout(orientation='horizontal', spacing=10, padding=dp(10), size_hint_y=None, height=dp(100))
        img = AsyncImage(source=item.get('image'), allow_stretch=True, keep_ratio=False, size_hint=(0.3, 1))
        card_layout.add_widget(img)
        name_label = Label(text=item.get('name'), size_hint_x=0.5, color=(0, 0, 0, 1))
        card_layout.add_widget(name_label)
        price_label = Label(text=f"${item.get('price')}", size_hint_x=None, width=dp(100), color=(0, 0, 0, 1))
        card_layout.add_widget(price_label)

        # Create a remove button (heart icon)
        remove_button = MDIconButton(icon="heart", pos_hint={"center_y": 0.5}, on_press=lambda btn, item=item: self.remove_item(item))
        card_layout.add_widget(remove_button)

        return card_layout

    def change_screen(self, screen_name):
        # Change the current screen in the ScreenManager
        self.manager.current = screen_name

    def remove_item(self, item):
        # Remove the item from the wishlist
        if item in wishlist:
            wishlist.remove(item)
            self.update_wishlist()
