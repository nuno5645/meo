from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from django.utils import timezone
from django.conf import settings
from django.core.management import call_command


class ProductListView(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(available=True)
        

            
        
        product_list = [
            {
                'id': product.id,
                'name': product.name,
                'points': product.points,
                'url': product.url,
                'available': product.available,
                'image_url': product.image_url,
                'link_url': product.link_url,
                'description': product.description,
                'stock': product.stock,
            }
            for product in products
        ]
        return Response(product_list, status=status.HTTP_200_OK)

class ProductDetailView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            product = Product.objects.get(id=id)
            product_data = {
                'id': product.id,
                'name': product.name,
                'points': product.points,
                'url': product.url,
                'available': product.available,
                'image_url': product.image_url,
                'link_url': product.link_url,
                'description': product.description,
                'stock': product.stock,
            }
            return Response(product_data)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)