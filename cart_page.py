import requests
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from requests.auth import HTTPBasicAuth


class CartPage(Screen):
    baseUrl = "YOUR_WEBSITE_URL"  # Define the base URL for WooCommerce API
    consumerKey = "YOUR_CONSUMER_KEY"  # Define the consumer key for WooCommerce API
    consumerSecret = "YOUR_CONSUMER_SECRET"  # Define the consumer secret for WooCommerce API

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_items = []

        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=0, padding=0)

        # App Bar
        app_bar = MDBoxLayout(
            adaptive_height=True,
            md_bg_color=(0, 0.6, 0.6, 1),
            padding=[dp(16), dp(8)],
            spacing=dp(8),
            size_hint_y=None,
            height=dp(56)
        )

        title_box = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            spacing=0
        )

        title = MDLabel(
            text="Shopping Cart",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(40)
        )

        subtitle = MDLabel(
            text="Review your items",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.7),
            font_style="Caption",
            size_hint_y=None,
            height=dp(16)
        )

        title_box.add_widget(title)
        title_box.add_widget(subtitle)
        app_bar.add_widget(title_box)

        # Scroll area for cart items
        scroll = ScrollView(size_hint=(1, 0.8))
        self.cart_items_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(8),
            spacing=dp(8)
        )
        self.cart_items_layout.bind(minimum_height=self.cart_items_layout.setter('height'))
        scroll.add_widget(self.cart_items_layout)

        # Total and checkout area
        bottom_area = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=[dp(16), dp(8)],
            md_bg_color=(1, 1, 1, 1)
        )

        self.total_label = MDLabel(
            text='Total: $0.00',
            font_style="H6",
            theme_text_color="Primary"
        )

        checkout_button = MDRaisedButton(
            text="CHECKOUT",
            md_bg_color=(0, 0.6, 0.6, 1),
            size_hint_x=1,
            height=dp(48)
        )
        checkout_button.bind(on_release=self.checkout)

        bottom_area.add_widget(self.total_label)
        bottom_area.add_widget(checkout_button)

        # Navigation bar
        nav_bar = self.create_navigation_bar()

        # Add all sections to main layout
        main_layout.add_widget(app_bar)
        main_layout.add_widget(scroll)
        main_layout.add_widget(bottom_area)
        main_layout.add_widget(nav_bar)

        self.add_widget(main_layout)

    def create_navigation_bar(self):
        nav_bar = MDBoxLayout(
            size_hint_y=None,
            height=dp(65),
            md_bg_color=(1, 1, 1, 1),
            padding=[0, dp(5), 0, dp(5)]
        )

        # Add navigation items
        nav_items = [
            ('home', 'Home', 'shop'),
            ('cards-heart', 'Favorite', 'wishlist'),
            ('cart', 'Cart', 'cart'),
            ('account', 'Profile', 'my_account')
        ]

        for icon, text, screen in nav_items:
            item = MDBoxLayout(orientation='vertical')

            icon_button = MDIconButton(
                icon=icon,
                pos_hint={'center_x': .5, 'center_y': .5}
            )
            icon_button.bind(on_release=lambda x, s=screen: self.change_screen(s))

            label = MDLabel(
                text=text,
                valign="center",
                halign="center",
                font_style="Caption"
            )

            # Highlight active tab
            if screen == 'cart':
                icon_button.theme_icon_color = "Custom"
                icon_button.icon_color = (0, 0.6, 0.6, 1)
                label.theme_text_color = "Custom"
                label.text_color = (0, 0.6, 0.6, 1)

            item.add_widget(icon_button)
            item.add_widget(label)
            nav_bar.add_widget(item)

        return nav_bar

    def add_to_cart(self, item):
        # Add an item to the cart and update the cart display
        self.cart_items.append(item)
        self.update_cart()

    def update_cart(self):
        self.cart_items_layout.clear_widgets()
        total_price = 0

        for index, item in enumerate(self.cart_items):
            # Create card for cart item
            card = MDCard(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(120),
                padding=dp(8),
                spacing=dp(8),
                elevation=1,
                radius=dp(4)
            )

            # Product image
            img = AsyncImage(
                source=item['image'],
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                allow_stretch=True,
                keep_ratio=True
            )

            # Product details layout
            details = MDBoxLayout(
                orientation='vertical',
                padding=[dp(8), 0],
                spacing=dp(4)
            )

            # Product name
            details.add_widget(MDLabel(
                text=item['name'],
                font_style='Subtitle1',
                size_hint_y=None,
                height=dp(30)
            ))

            # Price
            details.add_widget(MDLabel(
                text=f"${item['price']}",
                font_style='Body1',
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(20)
            ))

            # Quantity controls
            quantity_layout = MDBoxLayout(
                orientation='horizontal',
                spacing=dp(8),
                size_hint_y=None,
                height=dp(40)
            )

            quantity_layout.add_widget(
                MDIconButton(
                    icon='minus',
                    on_press=lambda x, idx=index: self.decrease_quantity(idx)
                )
            )

            quantity_label = MDLabel(
                text=str(item['quantity']),
                halign='center',
                size_hint_x=None,
                width=dp(40)
            )
            self.cart_items[index]['quantity_label'] = quantity_label
            quantity_layout.add_widget(quantity_label)

            quantity_layout.add_widget(
                MDIconButton(
                    icon='plus',
                    on_press=lambda x, idx=index: self.increase_quantity(idx)
                )
            )

            details.add_widget(quantity_layout)

            # Add image and details to card
            card.add_widget(img)
            card.add_widget(details)

            # Delete button
            card.add_widget(
                MDIconButton(
                    icon='delete',
                    on_press=lambda x, idx=index: self.delete_item(idx),
                    pos_hint={'center_y': 0.5}
                )
            )

            self.cart_items_layout.add_widget(card)
            total_price += float(item['price']) * item['quantity']

        self.total_label.text = f"Total: ${total_price:.2f}"

    def increase_quantity(self, index):
        # Increase the quantity of an item and update the cart
        self.cart_items[index]['quantity'] += 1
        self.cart_items[index]['quantity_label'].text = str(self.cart_items[index]['quantity'])
        self.update_cart()

    def decrease_quantity(self, index):
        # Decrease the quantity of an item and update the cart
        if self.cart_items[index]['quantity'] > 1:
            self.cart_items[index]['quantity'] -= 1
            self.cart_items[index]['quantity_label'].text = str(self.cart_items[index]['quantity'])
            self.update_cart()

    def delete_item(self, index):
        # Remove an item from the cart and update the cart
        del self.cart_items[index]
        self.update_cart()

    def checkout(self, instance):
        # Prepare and verify cart items data for checkout
        checkout_page = self.manager.get_screen('checkout')

        cart_items_data = []
        for item in self.cart_items:
            # Ensure 'id' is present and valid
            item_data = {
                'id': item.get('id'),
                'quantity': item.get('quantity')
            }
            if item_data['id'] is None:
                print(f"Warning: Item with missing ID detected: {item}")
            else:
                cart_items_data.append(item_data)

        cart_items_with_tags = []
        for item in cart_items_data:
            product_id = item.get('id')
            if product_id:
                # Fetch product details to get tags
                product_url = f'{self.baseUrl}/wp-json/wc/v3/products/{product_id}'
                print(f"Fetching product details from URL: {product_url}")

                try:
                    response = requests.get(product_url, auth=HTTPBasicAuth(self.consumerKey, self.consumerSecret))
                    if response.status_code == 200:
                        product_data = response.json()
                        tags = [tag['name'] for tag in product_data.get('tags', [])]
                        item['tags'] = tags
                        print(f"Product ID {product_id} Tags: {tags}")
                    else:
                        print(
                            f"Failed to fetch product details for ID {product_id}: {response.status_code} - {response.text}")
                except requests.RequestException as e:
                    print(f"Failed to fetch product details for ID {product_id}: {str(e)}")
            else:
                item['tags'] = []  # No tags if product ID is missing

        # Pass cart items with tags to checkout page
        checkout_page.cart_items = cart_items_data

        # Print cart items to verify
        print("Cart items with tags being sent to checkout page:", checkout_page.cart_items)

        # Switch to checkout page
        self.manager.current = 'checkout'

    def change_screen(self, screen_name):
        # Change the current screen
        self.manager.current = screen_name
