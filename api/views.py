import requests
from bs4 import BeautifulSoup
from .models import MyModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import urllib.request


class ScrapeData(APIView):
    def get(self, request, *args, **kwargs):
        url = 'https://app-9015f501-af0b-463a-b954-ab7059b01626.apps.meo.pt/api/v3StoreFront/GetStoreFrontProducts'

        # Headers based on the request information provided
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt-US;q=0.7,pt;q=0.6,nl;q=0.5',
            'Content-Type': 'application/json',
            'Origin': 'https://loja.meo.pt',
            'Referer': 'https://loja.meo.pt/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            # ... other headers as needed
        }

        # Payload based on the provided information
        payload = {
            'Refiners': [],
            'Sorting': 'Other',
            'PathName': '/Equipamentos/sensacoes'
        }

        # Make the POST request
        response = requests.post(url, headers=headers, json=payload)  # Using json parameter to automatically set content-type and serialize data

        # Check if the request was successful
        if response.status_code == 200:
            # If response is successful, parse the JSON data
            products = response.json()
        else:
            print(f"Failed to retrieve products, status code: {response.status_code}, response: {response.text}")

        products = products.get('Products', [])
        product_list = []
        
        for product in products:
            name = product.get('Name')
            points_cost = product.get('PointsPrice')
            available = not product.get('IsOutOfStock', True)  # Flip the boolean since we want to know if it's available
            image_url = product.get('ImageUrl')
            link_url = product.get('LinkUrl')
            description = product.get('Description')
            
            product_variants = product.get('ProductVariants', [])
            if product_variants:
                stock = product_variants[0].get('Stock')
            else:
                stock = 0

            my_model_product, created = MyModel.objects.get_or_create(
                name=name,
                defaults={
                    'name': name,
                    'points': points_cost,
                    'url': image_url,
                    'available': available,
                    'image_url': image_url,
                    'link_url': link_url,
                    'description': description,
                    'stock': stock
                }
            )
            
            product_list.append({
                'id': my_model_product.id,
                'name': name,
                'points_cost': points_cost,
                'available': available,
                'image_url': image_url,
                'link_url': link_url,
                'description': description[0],
                'stock': stock
            })
            
        print(product_list)
            
        # Return the scraped data as JSON
        return Response(product_list, status=status.HTTP_200_OK)