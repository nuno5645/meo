import requests
from bs4 import BeautifulSoup
from .models import Product, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import urllib.request
import json


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

            product, created = Product.objects.get_or_create(
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
                'id': product.id,
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
    
class ScrapeActivePoints(APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.get_or_create(id=1)
        try:
            # Define the URL and the header
            url = "https://cliente.meo.pt/api/PointsMember/GetPointsBalance"
            
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding' : 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt-US;q=0.7,pt;q=0.6,nl;q=0.5',
                'Connection': 'keep-alive',
                'Content-Length': '678',
                'Content-Type': 'application/json; charset=UTF-8',
                'Cookie': 'PtInfo=eyJVc2VyTmFtZSI6Im51bm8iLCJOYXZJZCI6IjRWcDRHeldrbzZheTVvUjdvejFoY3Uza1RCNEtMbUZOeVdkYktlU1Jic28iLCJJZFBJRCI6IlBUQ0xJRU5URSIsIkFsaWFzIjoibnRyamZlcnJlaXJhQGhvdG1haWwuY29tIn0%3D; _gcl_au=1.1.1879004380.1708178613; MEOAuthCampaign=1; wb_ga_clientId=undefined; _cen=1; UqZBpD3n3iPIDwJU9DmYiX2RRP8b4IMFfdzL9ZGclFjNHg__=v1MYg8g++CDS6; ASP.NET_SessionId=CfDJ8OSWnQ2HdkVPjhUr4zpDBaq%2F6nNQXjV45v67cMUobaeLyR2%2FKRWlVaeA2uBf7pgTJNRsN2PHpuMduohN%2B%2Bdr38iXuqs7lxCVGhbYf1VHmJLvcancMQ48smnxeL0wlb42WvUBuB2dq%2BT79QhbegJf9DYjF4jE6kx4vFxK2Sexa4n9; byside_webcare_tuid=u8r8b5rwa0gywh0bp9sipu7xz1gljgmkkubyfuknb6h1un2qvw; .AspNetCore.Cookies=CfDJ8OSWnQ2HdkVPjhUr4zpDBaphXn6bLy-Kqa6TEpbNYOgO9lgv6OVYGXcYHk8RPTCsQ7oamRVOMgE0M2LNqSZU_etKxOpYdI8w1Uv7E2ZTgc203eyxuz_qjPwNNYX7Hd0VIEwWhspemXwKSUlfLFiBcrFpEOwC_P9kI0AoUGw21GG7GTXdUFvL1a5IF84xo_tJfFfsBIxWb0_vKoRj6DOMbOcH535yOeKBhW3bLCugGcY9qkQV7ZFm3FSrK5GHFkhPFtwNmdYWFEUJV_wln_RMHwOeQo50Jr4gvU4csQ2qgzLgJNQPr9Olu-8jbrFfp_lTavldCkOJHYKeM4bGyp4d_C7KyiFfkV-LZGfunfGU4CvndiSg3VW45y1VczF1yvqp2TLCLlraWWNLk7z7MHbs4bCoj8VPhUSXTZzaXIhgzNnG-HaFaA8znFhnoYSGIONztpknLBjS6Rpt-7RrTxx3iDJzgnqWkAkp2UrF0hq0546we9dCvfWfTkRdxpOajwsvFQMN_JUODafZMSidsBlTcA6jLtOunyRCxejJEEAzGJt8Q7K-XSqQTF2z3m8UsrX0w1_cQcv-pyKBpYc7aznZ1b8f2vxtETYX7vanoN4sc0ZwOdA9CsERspKIxmWJwZFjp_kz841TW8Qcer1M43zrCw_q-tf05hxiorQe-dnivmC5OhhdkAinZbXmPE7c68cABH8M6Qq9BuIZllGaIHXmTXqr2tILOtr2hI5G7OH7CXItevTd2ms9bc1DwwTeNVwPyNYj-yWGlkC1kREWMlGXPi19_HnGtZDdlBXLn7k_PBJdlnZmVKfapt_ctzdT605l3SuDb7fnj983T8kejiwS4mL5uLwUd8BWaL6DlnMdb9CQqc-WHbvfRg5sQj1K_wBOj-fqWsyJ809Ns7mRBpDKIMRnStvpecS1yusY7R2tf_4m8OxvDdKtU_fY4fZyDiKLEqCibdG_dLptqxOrGFb9Mo9rZjj6Hte7RHnXQKy9OXc81kqHlVVXXErK4mUOF6RRoEHkYYSJi5A_GanfbzLBVFRk6A4etP-YAnvrF86yaY_nPgTlpUx7jRvbNY_yG-QpBJ5FsypnLKQEJM0Hbh0JYry6swfr18ltKQs14OkRnNBPCV8ILoHFS1XCd_pekCSfimW_aS6hImLr5LLXz0DvVoM_fRks8YxWnjciOEXJUTcZYdXhx24KyDokGINo6u7J54V5mZfcBwZE4_FiUkr7RlSl_fYytlCpuNnTimDGOjbnPhRFzOs38r89zcyhbYlegMqx_6LpeHYYeSKnJZC2Q3fEtMFEXqW-be2yA-K62K80wg7OYXnc5T9_hgOm7iU0Vxw9GiFtUlIRTjFwfV10NFrjkZhBGCqGoelyIiN15VSmghPx47vnGi9TbvD1aJ61XvhL4e4fiG_0NHwBeU-c2Ydqf79VFH6uvp6GTpHk199FLmmJubt6GyADoS0FfPcl7XjkOpDLt-u8PD4hkh04ZfY__fh2_tOxlMaxzTLL_TOmPeoIP8SL3_XWL-bJ_bmV3lEix_VXjK9qUWxPJQ3n27DRGj9OvajCCAN7aDDLKuIs0vH-O3P8RjYlLdNYYYV9N_n92PO6seCiMv38vb-5ElWzUe-Gh-tEt19k0LXgPV3f_u4OwcGlqwJ3goxDP4LBSG7dWNl1ZdcBk8U-Gd-0_5b8K0wwmB_zY0j7YO41HznGugnGlNganFjq809gcdU8fmD6C4aXzjlyv8t_K8GF8mhcjMbCRvig6QKnxpX1th76XG053LMG3E1uN5ziRxFOcDwksbOGy-xTLL9xfjuzL7ao4VvPP-M5faG6dCD75Tj8iiVpF2eInw-drbpqhKZHGjbHfZsl9toB2dTpBGn9gDvKNlXdbxziHAhR7bSf3GIVmucDAZ8G8pqdRICdsCLALxYGKU1LltOIAkbdaCL6qLlv5aLVkff4KR1x-hDHL3PwcijreeR7szajlXUA2IqwXjKeMPdsfAYy1H-S07EWTbcfZwbkFhPRJ6EAMPGDXQ-i3-RQYJlk0Aj6qy8y1HLO0AQXu69TICuR-bSgMcaeHKqBW4CDzX5J4T1zT_oTZmdEW3tjvta16OXMpUBGbOPXe5dzxAMv-FWbhI8xPn1nUQrJg8sfZdaby-md3NrOmDGtfObW_McsxAFJfV-jjNTByPXH4nUDP2qOrOqcm78IvP_9hh5y15FEVRKr0zv-e_B32ljLenMNTsz-UYeGe8c7qhWrZDGFcihcfOaI8FQ_mC7bLSqkwUyjrxSsu1kOzxGYkw0URo_11PgBFZSHTjUfVXrbeiO81A2de2sGGxNubOxhiyrAvNQPjiffpq-q-vVbWX_RB6iLkopkV-jNCtJqMgZDS_Sg4mKSyFscco-P70kLW2-I2t2Loii6Vo1Y3x6I874w3yV8X1Hpl7FkBDKqkzJ0Rd3wb2eiGAzj3bzN0rAheLQNbiUeJAMXeJ-GnIaWUGmJYUoF592SKLovYFI80Av1Q_y-machoav8qsz51aUD7oSAEB45IBB96Cix_BY1Fa_hCvD73qm2AOGUFnQlYkV4vsqX70vnOtGntgaz4wE',
                'Host': 'cliente.meo.pt',
                'Origin': 'https://cliente.meo.pt',
                'Referer': 'https://cliente.meo.pt/home-pacote-telemovel-pospago',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
                'sec-ch-ua-mobile': '?0',
                'sec-chua-platform': '"Windows"'
            }

            # Define the payload
            payload = {"Header":{"ID":"9f165a8a-17b4-b0a4-5dae-3f0360bdd86d","WidgetID":"4653ffe7-0482-4b71-8005-b0f483dafed5","Widdst":"MDNQU0cyOFg5bktnMVdsM1VwWFlOUWNHSkZheHo0TVJMSlgyRkF2a3N5Z2s2NGRtS1h1a0lHK1NHSTV1M2syVUg0MU9Pb1Axc1drd3VDbFdESTBqckJMU1Nla1Q2MmN2d0RETDl4NFRxSmREMHVVVEdNUVNUcmxHYWtzeEFXd3JXVmp6ZGRreUtpSmdtTlJYRGthUFBpU20yOTBqcmJJS2JlN280MU1nSE4zSmNoc1g5ZEhPeGdXYmJ3RGZDdHY2Wmxhb3dKS3M3MElOTVNrVVN4L3FDbTZVR3U5NDNHakRUUUp4NGZMSGprSHJDV05CNnNQc1FRL0x6YmFyVjE2UlZxNFNCTDRraXVRejlTWGxPYlJ1OXVWWmo0ekhpUzNxWDJlOHhtenNpMnlVcGFQTkdxOEsweXdHMzE1KzlIbTR0QVc0Q2pMWWJzSHI2NTBPYi9WYnVMTmpoV3hBL3VNRHArdE1IOHVNKzR5OTRvKzFCak02T3E4SEU4SitmQXMrVDQ="}}

            # Make the POST request
            response = requests.post(url, headers=headers, json=payload)
            # Check if the request was successful
            if response.status_code == 200:
                print("Request was successful.")
                # Handle the response content if needed, e.g., print it or parse JSON
                print(response.text)
            else:
                print(f"Request failed with status code: {response.status_code}")

            # Print out the JSON response if needed
            try:
                data_ = response.json()
                print(json.dumps(data, indent=4))
                #create a user and update the points
                try :
                    user.points = data_['pointsBalance']
                    user.save()
                except:
                    print("Failed to save points")
                
                data = {
                    "points": user.points
                }
                return Response(data, status=status.HTTP_200_OK)
            except ValueError:
                print("Response content is not in JSON format.")
                data = {
                    "points": user.points
                }
                return Response(data, status=status.HTTP_200_OK)
        except:
                user = User.objects.get(id=1)
                data = {
                    "points": user.points
                }
                return Response(data, status=status.HTTP_200_OK)