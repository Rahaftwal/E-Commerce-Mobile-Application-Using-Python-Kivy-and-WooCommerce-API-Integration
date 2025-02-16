from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
import requests
from kivy.storage.jsonstore import JsonStore
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivy.uix.widget import Widget
from kivymd.uix.relativelayout import MDRelativeLayout


class ShopPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.selected_product_id = None  # To keep track of the selected product
        self.selected_category = None  # To keep track of the selected category
        self.load_products()  # Load the products when the screen is initialized

    def load_products(self):
        print("Loading products...")
        url = 'YOUR_WEBSITE_URL/wp-json/wc/v3/products'
        auth = ('YOUR_CONSUMER_KEY', 'YOUR_CONSUMER_SECRET')

        if self.selected_category:
            url += f'?category={self.selected_category}'

        try:
            response = requests.get(url, auth=auth)
            response.raise_for_status()
            products = response.json()

            print("Products Data:", products)  # Print to inspect data structure

            if not products:
                print("No products found.")
            else:
                print(f"Loaded {len(products)} products.")

            store = JsonStore('settings.json')
            if 'purchased_product_tags' not in store:
                store.put('purchased_product_tags', tags=[])

            # Assuming purchased_product_tags is a list of tag names (strings)
            purchased_product_tags = store.get('purchased_product_tags')['tags']
            print("Purchased Product Tags:", purchased_product_tags)

            # Check if purchased_product_tags is an empty list
            if not purchased_product_tags:
                print("No purchased tags found. Please add purchased product tags.")

            def tag_similarity(product):

                product_tags = [tag['name'] for tag in product.get('tags', [])]
                return sum(tag in purchased_product_tags for tag in product_tags)

            sorted_products = sorted(products, key=lambda p: tag_similarity(p), reverse=True)
            print(f"Sorted Products Count: {len(sorted_products)}")

            self.ids.product_grid.clear_widgets()

            for product in sorted_products:
                self.add_product_widget(product)

        except requests.RequestException as e:
            print(f"Error fetching products: {e}")

        
        for product in products:
            print(f"Product: {product['name']}, Tags: {product.get('tags', [])}, Similarity: {tag_similarity(product)}")

    def add_product_widget(self, product):
        """
        Creates and adds a widget for a single product to the grid layout.
        """
        layout = self.create_product_layout(product)
        self.ids.product_grid.add_widget(layout)

    def create_product_layout(self, product):
        """
        Creates a layout for displaying a product, including its image, title, and price.
        """
        # Create card layout
        layout = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(220),
            padding=0,
            elevation=1,
            radius=dp(6),
            md_bg_color=[1, 1, 1, 1]
        )

        # Create image container with overlay for white text
        image_container = MDRelativeLayout(
            size_hint=(1, None),
            height=dp(130),
        )

        # Product image
        images = product.get('images', [])
        img_source = images[0].get('src', 'path/to/placeholder_image.png') if images else 'path/to/placeholder_image.png'

        img = AsyncImage(
            source=img_source,
            allow_stretch=True,
            keep_ratio=False,
        )

        # Add dark overlay for better text visibility
        overlay = MDBoxLayout(
            md_bg_color=[0, 0, 0, 0.4]  # Semi-transparent black overlay
        )

        # Product name on image
        image_title = MDLabel(
            text=product['name'],
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],  # White text
            size_hint_y=None,
            height=dp(44),
            padding=[dp(8), dp(4)],
            pos_hint={"center_x": 0.5, "y": 0},  # Position at bottom
            halign='left',
            font_style='Subtitle1'  # Using built-in KivyMD font style
        )

        image_container.add_widget(img)
        image_container.add_widget(overlay)
        image_container.add_widget(image_title)
        img.bind(on_touch_down=lambda instance, touch: self.on_image_click(instance, touch, product))

        # Content container
        content_container = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(90),
            padding=[dp(12), dp(8), dp(12), dp(8)],
            spacing=dp(4)
        )
        
        price = MDLabel(
            text=f"${product['price']}",
            size_hint_y=None,
            height=dp(24),
            halign='left',
            theme_text_color="Primary",
            font_style='H6'
        )

        # Action buttons
        action_box = MDBoxLayout(
            adaptive_height=True,
            spacing=0,
            padding=0,
            size_hint_y=None,
            height=dp(28)
        )
        
        cart_btn = MDIconButton(
            icon="cart",
            theme_icon_color="Custom",
            icon_color=(0, 0.6, 0.6, 1),
            pos_hint={"center_y": .5},
            size_hint_x=None,
            width=dp(30)
        )
        
        favorite_btn = MDIconButton(
            icon="heart-outline",
            theme_icon_color="Custom",
            icon_color=(0, 0.6, 0.6, 1),
            pos_hint={"center_y": .5},
            size_hint_x=None,
            width=dp(30)
        )

        spacer = Widget(size_hint_x=1)
        action_box.add_widget(spacer)
        action_box.add_widget(favorite_btn)
        action_box.add_widget(cart_btn)

        # Add content widgets
        content_container.add_widget(price)
        content_container.add_widget(action_box)

        # Add main containers
        layout.add_widget(image_container)
        layout.add_widget(content_container)

        return layout

    def on_image_click(self, instance, touch, product):
        """
        Handles click events on product images to navigate to the product details screen.
        """
        if instance.collide_point(*touch.pos):
            print(f"Product clicked: {product['name']}")
            self.selected_product_id = product['id']
            self.manager.current = 'product_details'
            product_details_screen = self.manager.get_screen('product_details')
            product_details_screen.load_product_details(product)

    def refresh_products(self):
        """
        Refreshes the list of products by reloading them.
        """
        print("Refresh button clicked")
        self.load_products()

    def change_screen(self, screen_name):
        """
        Changes the current screen to the specified screen name.
        """
        self.manager.current = screen_name
