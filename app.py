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
import json
from kivy.storage.jsonstore import JsonStore
# Window size is set to be resizable
Window.size = (400, 600)

class ProductCard(MDCard, RectangularRippleBehavior):
    def __init__(self, product_data, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = 1
        self.size_hint_y = None
        self.height = "200dp"  # Increased height to accommodate availability indicator
        self.padding = "8dp"
        self.spacing = "8dp"
        self.elevation = 5

        # BoxLayout for organizing the content
        box_layout = MDBoxLayout(orientation='vertical', spacing='8dp')
        self.add_widget(box_layout)

        # Add an image on top
        image_height_factor = 0.75  # Adjust this factor to your preference
        image = AsyncImage(source=product_data['image_url'], size_hint=(1, image_height_factor), allow_stretch=True)
        box_layout.add_widget(image)

        # Adjust the height of the label accordingly
        details = f"{product_data['name']}\nPoints Cost: {product_data['points_cost']}"
        label_height_factor = 1 - image_height_factor
        label = MDLabel(text=details, size_hint_y=None, height=self.height * label_height_factor, theme_text_color="Secondary")
        box_layout.add_widget(label)

        # Availability indicator
        availability = "Available" if product_data['available'] else "Not Available"
        availability_color = [0, 1, 0, 1] if product_data['available'] else [1, 0, 0, 1]  # RGB green or red
        availability_icon = "check-circle" if product_data['available'] else "close-circle"
        self.availability_label = OneLineIconListItem(text=availability)
        self.availability_label.add_widget(IconLeftWidget(icon=availability_icon, theme_text_color="Custom", text_color=availability_color))
        box_layout.add_widget(self.availability_label)

    def on_request_error(self, request, result):
        print("Error fetching data from the API:", request, result)
        # Add a UI element to indicate the error here

    def on_request_success(self, request, result):
        # Update the grid with the new data
        for item in result:
            product_box = ProductCard(product_data=item)
            self.grid_layout.add_widget(product_box)

    def refresh_grid(self, *args):
        # Clear the current grid
        self.grid_layout.clear_widgets()

        # Fetch the data from the API
        api_url = 'http://localhost/api/scrape_data/'
        UrlRequest(api_url, on_success=self.on_request_success, on_failure=self.on_request_error, on_error=self.on_request_error)

    def build(self):
        self.theme_cls.theme_style = "Dark"  # Use dark theme for a modern look
        self.theme_cls.primary_palette = "Gray"  # Set primary palette to grey
        self.title = 'Modern Grid App'

        # Main layout is a ScrollView to allow scrolling through the grid
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        self.grid_layout = MDGridLayout(cols=1, spacing="10dp", size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        scroll_view.add_widget(self.grid_layout)

        # Main BoxLayout
        self.main_layout = BoxLayout(orientation='vertical')
        self.main_layout.add_widget(scroll_view)

        # Refresh button at the bottom
        refresh_button = MDRaisedButton(
            text='Refresh',
            size_hint_y=None,
            height="50dp",
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.refresh_grid
        )
        self.main_layout.add_widget(refresh_button)

        # Initial data load
        self.refresh_grid()

        return self.main_layout

class ModernGridApp(MDApp):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_ids = set()
        
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        self.title = 'Modern Grid App'

        # Main layout is a ScrollView
        self.scroll_view = ScrollView(size_hint=(1, 1)) # Make the ScrollView fill its parent
        self.grid_layout = MDGridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)

        # Main BoxLayout
        self.main_layout = BoxLayout(orientation='vertical')
        self.main_layout.add_widget(self.scroll_view)

        # Refresh button at the bottom
        refresh_button = MDRaisedButton(
            text='Refresh',
            size_hint_y=None,
            height=dp(50),
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.refresh_grid
        )
        self.main_layout.add_widget(refresh_button)

        # Initial data load
        self.refresh_grid()

        # Bind the size of the main_layout to the window size to ensure resizing
        Window.bind(size=self._update_layout_size)

        return self.main_layout
    
    def _update_layout_size(self, instance, value):
        self.scroll_view.size = value

    def refresh_grid(self, *args):
        # Clear the current grid and the set of product IDs
        self.grid_layout.clear_widgets()
        self.product_ids.clear()  # Clear the set to accept the new batch of products

        # Fetch the data from the API
        api_url = 'http://localhost/api/scrape_data/'
        UrlRequest(api_url, on_success=self.on_request_success, on_failure=self.on_request_error, on_error=self.on_request_error)
        
    def save_data_to_cache(self, data):
        store = JsonStore('cache.json')
        store.put('offers', data=data)

    def load_data_from_cache(self):
        store = JsonStore('cache.json')
        if store.exists('offers'):
            return store.get('offers')['data']
        return None

    def on_request_success(self, request, result):
        # Update the grid with the new data
        for item in result:
            product_id = item.get('id')  # Assuming each product has a unique 'id' field
            if product_id not in self.product_ids:
                self.product_ids.add(product_id)  # Add the product ID to the set
                product_box = ProductCard(product_data=item)
                self.grid_layout.add_widget(product_box)
        
        # As the request was successful, save the data to cache
        self.save_data_to_cache(result)

    def on_request_error(self, request, result):
        print("Error fetching data from the API:", request, result)
        # Load cached data if available
        cached_data = self.load_data_from_cache()
        if cached_data:
            print("Loading data from cache.")
            self.on_request_success(request, cached_data)
        else:
            print("No cached data available.")
            # Add a UI element to indicate the error here

if __name__ == '__main__':
    ModernGridApp().run()