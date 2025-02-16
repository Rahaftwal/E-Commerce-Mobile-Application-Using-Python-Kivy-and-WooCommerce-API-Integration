from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
import requests
from requests.auth import HTTPBasicAuth

class CheckoutPage(Screen):
    baseUrl = "YOUR_WEBSITE_URL"
    consumerKey = "YOUR_CONSUMER_KEY"
    consumerSecret = "YOUR_CONSUMER_SECRET"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # User input fields
        self.email_input = TextInput(hint_text='Email', size_hint_y=0.1)
        layout.add_widget(self.email_input)

        self.password_input = TextInput(hint_text='Password', password=True, size_hint_y=0.1)
        layout.add_widget(self.password_input)

        self.first_name_input = TextInput(hint_text='First Name', size_hint_y=0.1)
        layout.add_widget(self.first_name_input)

        self.last_name_input = TextInput(hint_text='Last Name', size_hint_y=0.1)
        layout.add_widget(self.last_name_input)

        self.address1_input = TextInput(hint_text='Address 1', size_hint_y=0.1)
        layout.add_widget(self.address1_input)

        self.address2_input = TextInput(hint_text='Address 2', size_hint_y=0.1)
        layout.add_widget(self.address2_input)

        self.phone_input = TextInput(hint_text='Phone Number', size_hint_y=0.1)
        layout.add_widget(self.phone_input)

        self.city_input = TextInput(hint_text='City', size_hint_y=0.1)
        layout.add_widget(self.city_input)

        self.order_button = Button(text='Place Order', size_hint_y=0.2)
        self.order_button.bind(on_press=self.place_order)
        layout.add_widget(self.order_button)

        self.add_widget(layout)

        self.cart_items = []  # This will be assigned from the Cart Page

    def place_order(self, instance):
        # Collect user data
        email = self.email_input.text
        password = self.password_input.text
        first_name = self.first_name_input.text
        last_name = self.last_name_input.text
        address1 = self.address1_input.text
        address2 = self.address2_input.text
        phone = self.phone_input.text
        city = self.city_input.text

        # Debug prints for input values
        print(f"Email: {email}")
        print(f"First Name: {first_name}, Last Name: {last_name}")
        print(f"Address1: {address1}, Address2: {address2}, City: {city}")
        print(f"Phone: {phone}")

        # Check if email and password are provided
        if email and password:
            user_id = self.login_user(email, password)
        else:
            store = JsonStore('settings.json')
            if 'user' in store and not store['user']['is_guest']:
                user_id = store['user']['user_id']
            else:
                user_id = None

        cart_items = self.cart_items

        # Debug print statements to verify cart items
        print("Cart Items:", cart_items)

        # Create order data
        order_data = {
            'payment_method': 'cod',
            'payment_method_title': 'Cash on Delivery',
            'set_paid': False,
            'billing': {
                'first_name': first_name,
                'last_name': last_name,
                'address_1': address1,
                'address_2': address2,
                'city': city,
                'phone': phone,
                'email': email,
            },
            'shipping': {
                'first_name': first_name,
                'last_name': last_name,
                'address_1': address1,
                'address_2': address2,
                'city': city,
            },
            'line_items': [{'product_id': item.get('id'), 'quantity': item.get('quantity')} for item in cart_items if
                           'id' in item and 'quantity' in item]
        }

        # Debug print for order data
        print("Order Data:", order_data)

        url = f'{self.baseUrl}/wp-json/wc/v3/orders'
        try:
            response = requests.post(url, auth=HTTPBasicAuth(self.consumerKey, self.consumerSecret), json=order_data)
            if response.status_code == 201:
                print("Order placed successfully")

                # Extract tags from cart items and update stored tags
                product_tags = self.extract_product_tags(cart_items)
                print("Extracted Product Tags:", product_tags)
                self.update_tags_in_store(product_tags)

                self.manager.get_screen('cart').cart_items = []
                self.manager.get_screen('cart').update_cart()
                self.manager.current = 'shop'
            else:
                print(f"Failed to place order: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print(f"Failed to place order: {str(e)}")

    def login_user(self, email, password):
        url = f'{self.baseUrl}/wp-json/wc/v3/customers'
        try:
            response = requests.get(url, auth=HTTPBasicAuth(self.consumerKey, self.consumerSecret))
            if response.status_code == 200:
                customers = response.json()
                for customer in customers:
                    if customer['email'] == email and customer['password'] == password:
                        # Save user details and return user ID
                        store = JsonStore('settings.json')
                        store.put('user', user_id=customer['id'], is_guest=False)

                        # Debug print for successful login
                        print(f"User {customer['id']} logged in successfully")

                        # Save purchased tags upon login
                        product_tags = self.extract_product_tags(self.cart_items)
                        print("Extracted Product Tags on Login:", product_tags)
                        self.update_tags_in_store(product_tags)

                        return customer['id']
                print("Incorrect email or password")
            else:
                print(f"Failed to login: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print(f"Failed to login: {str(e)}")
        return

    def extract_product_tags(self, cart_items):
        # Extract tags from each product in the cart
        product_tags = set()  # Use a set to avoid duplicates

        for item in cart_items:
            # Debug print to check the structure of each cart item
            print("Cart Item:", item)

            if 'tags' in item and isinstance(item['tags'], list):
                # Check if 'tags' is a list and handle accordingly
                print("Tags Found:", item['tags'])  # Check the tags for the item
                for tag in item['tags']:
                    if tag not in product_tags:
                        product_tags.add(tag)
            else:
                print("No tags found in this cart item or tags is not a list")

        # Debug print for extracted product tags
        print("Extracted Tags after processing:", list(product_tags))

        return list(product_tags)

    def update_tags_in_store(self, new_tags):
        store = JsonStore('settings.json')
        # Check if 'purchased_product_tags' exists in the store
        if 'purchased_product_tags' in store:
            existing_tags = store.get('purchased_product_tags').get('tags', [])
        else:
            existing_tags = []

        # Debug print for existing and new tags
        print("Existing Tags:", existing_tags)
        print("New Tags:", new_tags)

        # Merge new tags without duplicating
        updated_tags = list(set(existing_tags + new_tags))

        # Debug print for updated tags
        print("Updated Tags:", updated_tags)

        # Save updated tags back to the store
        store.put('purchased_product_tags', tags=updated_tags)
