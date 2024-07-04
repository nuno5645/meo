from .views import ScrapeData, ScrapeActivePoints, ProductDetailView
#import path from django.urls
from django.urls import path


urlpatterns = [
    path('scrape_data/', ScrapeData.as_view(), name='scrape_data'),
    path('points/', ScrapeActivePoints.as_view(), name='points'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),

]