from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
from kivy.core.window import Window
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen
Window.size = (400, 650)

class ProductCard(MDCard, RectangularRippleBehavior):
    def __init__(self, product_data, **kwargs):
        super().__init__(**kwargs)
        self.product_data = product_data
        self.size_hint_x = 1
        self.size_hint_y = None
        self.height = "200dp"
        self.padding = "8dp"
        self.spacing = "8dp"
        self.elevation = 5
        self.orientation = "vertical"

        image = AsyncImage(source=self.product_data['image_url'], size_hint=(1, 0.75), allow_stretch=True)
        self.add_widget(image)

        details = f"{self.product_data['name']}\nPoints Cost: {self.product_data['points_cost']}"
        label = MDLabel(text=details, size_hint_y=None, height="48dp", theme_text_color="Secondary")
        self.add_widget(label)

        availability = "Available" if self.product_data['available'] else "Not Available"
        availability_color = [0, 1, 0, 1] if self.product_data['available'] else [1, 0, 0, 1]
        availability_icon = "check-circle" if self.product_data['available'] else "close-circle"
        self.availability_label = OneLineIconListItem(text=availability)
        self.availability_label.add_widget(IconLeftWidget(icon=availability_icon, theme_text_color="Custom", text_color=availability_color))
        self.add_widget(self.availability_label)

    def on_release(self):
        app = MDApp.get_running_app()
        app.show_product_details(self.product_data)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        self.product_ids = set()
        self.grid_layout = MDGridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.grid_layout)
        
        self.add_widget(scroll_view)
        
        # Refresh button at the bottom
        refresh_button = MDRaisedButton(
            text='Refresh',
            size_hint_y=None,
            height=dp(50),
            md_bg_color=MDApp.get_running_app().theme_cls.primary_color,
            on_release=self.refresh_grid
        )
        self.add_widget(refresh_button)

        self.refresh_grid()

    def refresh_grid(self, *args):
        self.grid_layout.clear_widgets()
        self.product_ids.clear()
        
        api_url = 'http://localhost/api/scrape_data/'
        UrlRequest(api_url, on_success=self.on_request_success, on_failure=self.on_request_error, on_error=self.on_request_error)
    
    def on_request_success(self, request, result):
        for item in result:
            product_id = item.get('id')
            if product_id not in self.product_ids:
                self.product_ids.add(product_id)
                product_box = ProductCard(product_data=item)
                self.grid_layout.add_widget(product_box)
        
    def on_request_error(self, request, result):
        print("Error fetching data from the API:", request, result)

class ProductDetailsScreen(Screen):
    def __init__(self, name, product_data, **kwargs):
        super().__init__(name=name, **kwargs)
        self.product_data = product_data
        self.create_product_details()

    def create_product_details(self):
        layout = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        self.add_widget(layout)

        # Add widgets for product details
        image = AsyncImage(source=self.product_data['image_url'], size_hint=(1, 0.3), allow_stretch=True)
        layout.add_widget(image)

        details_label = MDLabel(
            text=f"{self.product_data['name']}\nPoints Cost: {self.product_data['points_cost']}\nDescription:{self.product_data['description']}\nStock: {self.product_data['stock']}",
            size_hint_y=None,
            theme_text_color="Secondary"
        )
        layout.add_widget(details_label)

        back_button = MDRaisedButton(
            text="Back",
            size_hint=(1, None),
            height=dp(48),
            on_release=self.go_back
        )
        layout.add_widget(back_button)

    def go_back(self, *args):
        MDApp.get_running_app().root.current = 'main'

class ModernGridApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        self.title = 'Modern Grid App'

        self.screen_manager = ScreenManager(transition=SlideTransition())
        self.main_screen = MainScreen()
        self.screen_manager.add_widget(self.main_screen)

        return self.screen_manager

    def show_product_details(self, product_data):
        # Generate a unique screen name for each product detail screen
        screen_name = f"product_details_{product_data['id']}"

        # Check if the screen already exists and remove it
        if self.screen_manager.has_screen(screen_name):
            self.screen_manager.remove_widget(self.screen_manager.get_screen(screen_name))

        # Create a new product details screen with a unique name
        details_screen = ProductDetailsScreen(name=screen_name, product_data=product_data)
        self.screen_manager.add_widget(details_screen)
        self.screen_manager.current = screen_name

if __name__ == '__main__':
    ModernGridApp().run()