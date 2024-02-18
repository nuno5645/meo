from .views import ScrapeData, ScrapeActivePoints
#import path from django.urls
from django.urls import path


urlpatterns = [
    path('scrape_data/', ScrapeData.as_view(), name='scrape_data'),
    path('points/', ScrapeActivePoints.as_view(), name='points'),
]