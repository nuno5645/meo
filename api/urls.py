from .views import ScrapeData
#import path from django.urls
from django.urls import path


urlpatterns = [
    path('scrape_data/', ScrapeData.as_view(), name='scrape_data'),
]