from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

# Import custom screen classes
from cart_page import CartPage
from checkoutPage import CheckoutPage
from product_details_page import ProductDetailsPage
from shop_page import ShopPage
from splashscreen import SplashScreen
from onboardingscreen import OnboardingScreen
from selection_operation import SelectionOperationScreen
from sign_in import SignInScreen
from sign_up import SignUpScreen
from kivy.core.window import Window
from my_account_page import MyAccountScreen
from wishlist_page import WishlistPage
from kivy.lang import Builder
from kivymd.app import MDApp
# Set the initial window size
Window.size = (380, 640)

class MyApp(MDApp):
    def build(self):
        # Load KV files for the app's UI components
        Builder.load_file('shop.kv')
        Builder.load_file('wishlist_page.kv')
        # Builder.load_file('product_details.kv') # Uncomment if needed

        # Set the application window title
        self.title = 'E-Commerce Application'

        # Set the application window icon
        self.icon = 'images/spashscreen.png'

        # Initialize JsonStore to handle session data
        self.store = JsonStore('session.json')

        # Create an instance of ScreenManager to manage screen transitions
        sm = ScreenManager()

        # Add different screens to the ScreenManager
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(OnboardingScreen(name='onboarding'))
        sm.add_widget(SelectionOperationScreen(name='selection_operation'))
        sm.add_widget(SignInScreen(name='sign_in'))
        sm.add_widget(SignUpScreen(name='sign_up'))
        sm.add_widget(ShopPage(name='shop'))
        sm.add_widget(ProductDetailsPage(name='product_details'))
        sm.add_widget(WishlistPage(name='wishlist'))
        sm.add_widget(CartPage(name='cart'))
        sm.add_widget(MyAccountScreen(name='my_account'))
        sm.add_widget(CheckoutPage(name='checkout'))

        # Return the ScreenManager instance to be used by the App
        return sm

# Run the application if this script is executed
if __name__ == '__main__':
    MyApp().run()
