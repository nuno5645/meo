from .views import ProductListView, ProductDetailView
#import path from django.urls
from django.urls import path


urlpatterns = [
    path('scrape_data/', ProductListView.as_view(), name='scrape_data'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
]