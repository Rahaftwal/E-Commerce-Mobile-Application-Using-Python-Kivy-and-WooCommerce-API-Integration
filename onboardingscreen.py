from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.metrics import dp


class OnboardingScreen(Screen):
    def __init__(self, **kwargs):
        # Initialize the Screen with any passed keyword arguments
        super().__init__(**kwargs)

        # Define color scheme
        self.primary_color = (0, 0.7, 0.6, 1)  # Teal color
        self.text_color = (0.2, 0.2, 0.2, 1)
        self.secondary_color = (0.7, 0.7, 0.7, 1)

        # Create main layout
        layout = FloatLayout()

        # Set background
        with layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        # Onboarding content
        self.pages = [
            {
                'image': 'images/onbpoarding/on1.png',
                'title': 'Welcome to Our App!',
                'description': 'Discover a world of amazing products'
            },
            {
                'image': 'images/onbpoarding/2.png',
                'title': 'Shop with Ease',
                'description': 'Find your favorite products quickly and easily'
            },
            {
                'image': 'images/onbpoarding/3.png',
                'title': 'Get Started',
                'description': 'Experience a unique shopping journey'
            }
        ]
        
        self.page_number = 0
        
        # Add feature image
        self.image = Image(
            size_hint=(None, None),
            size=(dp(250), dp(250)),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        
        # Add title
        self.title_label = Label(
            font_size=dp(24),
            bold=True,
            color=self.primary_color,
            size_hint=(None, None),
            size=(dp(400), dp(50)),
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )
        
        # Add description
        self.desc_label = Label(
            font_size=dp(16),
            color=self.text_color,
            size_hint=(None, None),
            size=(dp(300), dp(80)),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        
        # Add page indicators (dots)
        self.dots_layout = BoxLayout(
            size_hint=(None, None),
            size=(dp(150), dp(30)),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            spacing=dp(15)  # Increased spacing between dots
        )
        self._create_dots()
        
        # Next button
        self.next_button = Button(
            text='Next',
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5, 'center_y': 0.15},
            background_color=self.primary_color,
            background_normal='',
            color=(1, 1, 1, 1),  # White text
            bold=True
        )
        self.next_button.bind(on_press=self.next_page)
        
        # Add all elements to layout
        layout.add_widget(self.image)
        layout.add_widget(self.title_label)
        layout.add_widget(self.desc_label)
        layout.add_widget(self.dots_layout)
        layout.add_widget(self.next_button)
        
        self.add_widget(layout)
        self._update_content()

    def _create_dots(self):
        """Create page indicator dots"""
        self.dots = []
        for i in range(len(self.pages)):
            dot = Button(
                size_hint=(None, None),
                size=(dp(12), dp(12)),  # Slightly larger dots
                background_color=self.secondary_color,
                background_normal='',
            )
            self.dots_layout.add_widget(dot)
            self.dots.append(dot)
    
    def _update_content(self):
        """Update content with transition animation"""
        page = self.pages[self.page_number]
        
        anim = Animation(opacity=0, duration=0.2) + Animation(opacity=1, duration=0.4)
        
        self.image.source = page['image']
        self.title_label.text = page['title']
        self.desc_label.text = page['description']
        
        # Update page indicators
        for i, dot in enumerate(self.dots):
            dot.background_color = self.primary_color if i == self.page_number else self.secondary_color
        
        # Update button text on last page
        if self.page_number == len(self.pages) - 1:
            self.next_button.text = 'Get Started'
        
        anim.start(self.image)
        anim.start(self.title_label)
        anim.start(self.desc_label)

    def _update_bg_rect(self, instance, value):
        """Update background rectangle size and position"""
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def next_page(self, instance):
        """Handle next page navigation"""
        if self.page_number < len(self.pages) - 1:
            self.page_number += 1
            self._update_content()
        else:
            store = JsonStore('settings.json')
            store.put('onboarding_shown', shown=True)
            self.manager.current = 'selection_operation'
