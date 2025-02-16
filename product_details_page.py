import re
import requests
from kivy.metrics import dp
from kivy.properties import get_color_from_hex
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivymd.uix.relativelayout import MDRelativeLayout

# Global variable to store wishlist items
wishlist = []


class ProductDetailsPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set up background color
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Main layout for the screen
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=2)
        self.add_widget(self.main_layout)

        self.app_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=5)

        # Replace Button with MDIconButton for back navigation
        self.back_button = MDIconButton(icon='arrow-left', icon_color=(0, 0, 0, 1), size_hint_x=None, width=100)
        self.back_button.bind(on_press=self.go_back)
        self.app_bar.add_widget(self.back_button)

        # Title label
        self.title_label = MDLabel(text='Product Details', size_hint_x=1, color=(0, 0, 0, 1))
        self.app_bar.add_widget(self.title_label)

        self.main_layout.add_widget(self.app_bar)

        # ScrollView to contain details_layout
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.details_layout = BoxLayout(orientation='vertical', spacing=1, size_hint_y=None)
        self.details_layout.bind(minimum_height=self.details_layout.setter('height'))
        self.scroll_view.add_widget(self.details_layout)

        self.main_layout.add_widget(self.scroll_view)

        # Initialize other attributes
        self.product_image = None
        self.price_label = None
        self.variable_buttons = []
        self.selected_variation = None
        self.variations = {}
        self.product = None
        self.quantity = 1  # Default quantity

    def _update_rect(self, instance, value):
        """Update the rectangle size and position to match the widget size and position."""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def load_product_details(self, product):
        self.product = product
        self.details_layout.clear_widgets()

        # Image container with overlay for title
        image_container = MDRelativeLayout(
            size_hint_y=None,
            height=dp(300),  # Slightly smaller image
        )
        
        # Product image
        img_source = product.get('images', [{}])[0].get('src', 'path/to/placeholder_image.png')
        img = AsyncImage(
            source=img_source,
            allow_stretch=True,
            keep_ratio=False,
        )
        
        # Dark overlay at the bottom
        overlay = MDBoxLayout(
            size_hint_y=None,
            height=dp(60),  # Smaller overlay
            md_bg_color=[0, 0, 0, 0.4],  # More transparent
            pos_hint={"center_x": 0.5, "y": 0}
        )

        # Title on image
        title = MDLabel(
            text=product.get('name', 'Product Name'),
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            size_hint_y=None,
            height=dp(60),
            padding=[dp(16), dp(10)],
            pos_hint={"center_x": 0.5, "y": 0}
        )

        image_container.add_widget(img)
        image_container.add_widget(overlay)
        image_container.add_widget(title)
        self.details_layout.add_widget(image_container)

        # Price and quantity container
        info_container = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            padding=[dp(16), dp(10)],
            spacing=dp(10),
            md_bg_color=[1, 1, 1, 1]
        )

        # Price with smaller text
        price = MDLabel(
            text=f"${product.get('price', '0')}",
            font_style='H6',  # Even smaller font
            theme_text_color="Custom",
            text_color=(0, 0.6, 0.6, 1),
            size_hint_y=None,
            height=dp(30)
        )
        info_container.add_widget(price)
        self.price_label = price

        # Quantity selector with improved design
        quantity_layout = MDBoxLayout(
            adaptive_height=True,
            spacing=dp(15),
            padding=[0, dp(8)],
            size_hint_y=None,
            height=dp(40)
        )

        # Quantity label with improved style
        quantity_label = MDLabel(
            text="Quantity",
            theme_text_color="Secondary",
            font_style="Body2",  # Smaller font
            size_hint_x=None,
            width=dp(60)
        )

        # Counter box with improved design
        counter_box = MDBoxLayout(
            size_hint=(None, None),
            size=(dp(90), dp(32)),  # Smaller size
            padding=[dp(4), 0],
            spacing=dp(4),
            radius=[dp(16)],  # Rounded corners
            md_bg_color=(0.95, 0.95, 0.95, 1)  # Light gray background
        )

        self.minus_button = MDIconButton(
            icon='minus',
            theme_icon_color="Custom",
            icon_color=(0, 0.6, 0.6, 1),  # Teal color
            size_hint=(None, None),
            size=(dp(24), dp(24)),  # Smaller icon
            pos_hint={"center_y": .5},
            on_press=self.decrease_quantity
        )
        
        self.quantity_label = MDLabel(
            text=str(self.quantity),
            halign='center',
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),  # Black text
            size_hint_x=None,
            width=dp(30),
            pos_hint={"center_y": .5}
        )
        
        self.plus_button = MDIconButton(
            icon='plus',
            theme_icon_color="Custom",
            icon_color=(0, 0.6, 0.6, 1),  # Teal color
            size_hint=(None, None),
            size=(dp(24), dp(24)),  # Smaller icon
            pos_hint={"center_y": .5},
            on_press=self.increase_quantity
        )

        counter_box.add_widget(self.minus_button)
        counter_box.add_widget(self.quantity_label)
        counter_box.add_widget(self.plus_button)

        quantity_layout.add_widget(quantity_label)
        quantity_layout.add_widget(counter_box)
        info_container.add_widget(quantity_layout)

        self.details_layout.add_widget(info_container)

        # Description section with card style
        if product.get('description'):
            description_card = MDBoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(200),
                padding=dp(16),
                spacing=dp(10),
                md_bg_color=[1, 1, 1, 1],  # White background
                radius=[10, 10, 10, 10]
            )

            description_title = MDLabel(
                text="Description",
                font_style='H6',
                theme_text_color="Custom",
                text_color=(0, 0.6, 0.6, 1),  # Teal color
                size_hint_y=None,
                height=dp(30)
            )
            description_card.add_widget(description_title)

            description_text = self.strip_html(product.get('description', ''))
            description = MDLabel(
                text=description_text,
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(160)
            )
            description_card.add_widget(description)

            self.details_layout.add_widget(MDBoxLayout(size_hint_y=None, height=dp(20)))  # Spacing
            self.details_layout.add_widget(description_card)

        actions_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        # Create the wishlist button with an icon
        wishlist_button = MDIconButton(
            icon='heart',
            theme_icon_color='Custom',
            icon_color=(1, 0, 0, 1),  # Red color for the icon
            size_hint=(0.5, 1)
        )
        wishlist_button.bind(on_press=self.add_to_wishlist)
        actions_layout.add_widget(wishlist_button)

        # Create the cart button with an icon
        cart_button = MDIconButton(
            icon='cart',
            theme_icon_color='Custom',
            icon_color=(0, 0, 0, 1),  # Black color for the icon
            size_hint=(0.5, 1)
        )
        cart_button.bind(on_press=self.add_to_cart)
        actions_layout.add_widget(cart_button)

        # Add the actions layout to your details layout
        self.details_layout.add_widget(actions_layout)

    def fetch_variations(self, product_id):
        """Fetch and store product variations from the API."""
        url = f'YOUR_WEBSITE_URL/wp-json/wc/v3/products/{product_id}/variations'
        auth = ('YOUR_CONSUMER_KEY', 'YOUR_CONSUMER_SECRET')
        response = requests.get(url, auth=auth)
        variations_data = response.json()

        self.variations = {var['attributes'][0]['option']: var['price'] for var in variations_data}
        print(f"Variations loaded: {self.variations}")

    def on_variation_select(self, instance):
        """Handle selection of a variation and update the price accordingly."""
        selected_value = instance.text
        print(f"Selected variation: {selected_value}")

        if self.selected_variation:
            self.selected_variation.background_color = (1, 1, 1, 1)  # Reset previous selection

        self.selected_variation = instance
        self.selected_variation.background_color = (0.8, 0.8, 0.8, 1)  # Highlight selected variation

        # Update price based on selected variation
        new_price = self.variations.get(selected_value, '0')
        self.price_label.text = f"Price: ${new_price}"

    def strip_html(self, text):
        """Remove HTML tags from text."""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def add_to_wishlist(self, instance):
        """Add the current product to the wishlist."""
        if self.product:
            product_data = {
                'name': self.product.get('name'),
                'image': self.product.get('images', [{}])[0].get('src', 'path/to/placeholder_image.png'),
                'price': self.product.get('price', '0')
            }
            wishlist.append(product_data)
            print(f"Added to wishlist: {product_data}")

            # Update wishlist page
            wishlist_page = self.manager.get_screen('wishlist')
            wishlist_page.update_wishlist()

    def add_to_cart(self, instance):
        """Add the current product to the cart."""
        if self.product:
            cart_page = self.manager.get_screen('cart')

            # Extract tags ensuring they are in name format
            tags = self.product.get('tags', [])
            tags = [tag['name'] if isinstance(tag, dict) and 'name' in tag else str(tag) for tag in tags]

            product_details = {
                'id': self.product.get('id'),
                'name': self.product.get('name'),
                'image': self.product.get('images', [{}])[0].get('src', 'path/to/placeholder_image.png'),
                'price': self.product.get('price', '0'),
                'quantity': self.quantity,
                'tags': tags
            }

            cart_page.add_to_cart(product_details)

            # Print product details
            print("Added to cart with the following details:")
            print(f"ID: {product_details['id']}")
            print(f"Name: {product_details['name']}")
            print(f"Image: {product_details['image']}")
            print(f"Price: {product_details['price']}")
            print(f"Quantity: {product_details['quantity']}")
            print(f"Tags: {', '.join(product_details['tags'])}")

    def increase_quantity(self, instance):
        """Increase the quantity by 1 and update the label."""
        self.quantity += 1
        self.quantity_label.text = str(self.quantity)

    def decrease_quantity(self, instance):
        """Decrease the quantity by 1 if greater than 1 and update the label."""
        if self.quantity > 1:
            self.quantity -= 1
            self.quantity_label.text = str(self.quantity)

    def go_back(self, instance):
        """Navigate back to the previous screen."""
        self.manager.current = 'shop'

    def add_variations(self, attributes):
        """Add variations to the product details page."""
        variable_layout = MDBoxLayout(orientation='horizontal', spacing=10, padding=dp(10), size_hint_y=None,
                                      height=70, )
        for attribute in attributes:
            if attribute['variation']:
                attr_name = attribute['name']
                attr_values = attribute['options']
                attr_layout = MDBoxLayout(orientation='horizontal', spacing=10)
                attr_label = MDLabel(
                    text=f"{attr_name}: ",
                    size_hint_x=None,
                    width=dp(50),
                    halign='left',
                    theme_text_color='Primary'
                )
                attr_layout.add_widget(attr_label)
                for value in attr_values:
                    btn = MDRaisedButton(
                        text=value,
                        size_hint_x=None,
                        size_hint_y=None,
                        height=dp(40),
                        on_release=self.on_variation_select,
                        md_bg_color=get_color_from_hex("#A5D6A7"),
                    )

                    attr_layout.add_widget(btn)
                    self.variable_buttons.append(btn)

                # Adjust button width dynamically
                total_buttons = len(attr_values)
                button_width = 1 / total_buttons if total_buttons > 0 else 1
                for btn in self.variable_buttons:
                    btn.size_hint_x = button_width

                attr_layout.add_widget(attr_layout)
        self.details_layout.add_widget(variable_layout)
