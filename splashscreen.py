from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.storage.jsonstore import JsonStore

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        # Initialize the parent class
        super().__init__(**kwargs)

        # Create a vertical BoxLayout to hold widgets
        layout = BoxLayout(orientation='vertical')

        # Set up the canvas for the layout to draw a white background
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # Set the color to white
            self.rect = Rectangle(size=layout.size, pos=layout.pos)  # Create a rectangle with the same size and position as the layout

        # Update the rectangle size and position when the layout size or position changes
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Load an image and add it to the layout
        img = Image(source='images/shop.png')
        layout.add_widget(img)

        # Schedule the switch to the onboarding screen after 3 seconds
        Clock.schedule_once(self.switch_to_onboarding, 3)

        # Add the layout to the screen
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        # Update the rectangle size and position when the layout changes
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def switch_to_onboarding(self, dt):
        # Switch to the onboarding screen
        self.manager.current = 'onboarding'
