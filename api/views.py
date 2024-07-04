from .models import Product, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .MeoService import MeoService  # Import the service class
from django.http import JsonResponse

class ScrapeData(APIView):
    def get(self, request, *args, **kwargs):
        products_data = MeoService.get_store_products()
        if not products_data:
            return Response({"error": "Failed to retrieve products"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        products = products_data.get('Products', [])
        product_list = []

        for product in products:
            name = product.get('Name')
            points_cost = product.get('PointsPrice')
            available = not product.get('IsOutOfStock', True)
            image_url = product.get('ImageUrl')
            link_url = product.get('LinkUrl')
            description = product.get('Description')
            product_variants = product.get('ProductVariants', [])
            stock = product_variants[0].get('Stock') if product_variants else 0

            product_obj, created = Product.objects.get_or_create(
                name=name,
                defaults={
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
                'id': product_obj.id,
                'name': name,
                'points_cost': points_cost,
                'available': available,
                'image_url': image_url,
                'link_url': link_url,
                'description': description,
                'stock': stock
            })

        return Response(product_list, status=status.HTTP_200_OK)


class ScrapeActivePoints(APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.get_or_create(id=1)[0]
        points_data = MeoService.get_points_balance()

        if points_data:
            user.points = points_data.get('pointsBalance', user.points)
            user.save()

        data = {
            "points": user.points
        }
        return Response(data, status=status.HTTP_200_OK)
    

class ProductDetailView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            product = Product.objects.get(id=id)
            product_data = {
                'id': product.id,
                'name': product.name,
                'points_cost': product.points,
                'available': product.available,
                'image_url': product.image_url,
                'link_url': product.link_url,
                'description': product.description,
                'stock': product.stock
            }
            return JsonResponse(product_data)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)