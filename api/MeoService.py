import requests
from bs4 import BeautifulSoup

class MeoScraper:
    @staticmethod
    def scrape_sensacoes_meos():
        url = "https://loja.meo.pt/sensacoes-meos"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        product_items = soup.select('.sf-item')
        
        for item in product_items:
            product = {}
            product['name'] = item.select_one('.sf-item-name h2').text.strip()
            product['points'] = int(item.select_one('.sf-item-footer-item .sf-item-details span').text.strip())
            product['image_url'] = item.select_one('.sf-item-image img')['src']
            product['link_url'] = item.select_one('a.sf-item-wrapper')['href']
            product['available'] = 'no-stock' not in item.select_one('a.sf-item-wrapper').get('class', [])
            product['url'] = url
            product['description'] = item.select_one('.sf-item-name h2')['title']
            product['stock'] = 0 if not product['available'] else 1  # Assuming 1 if available, 0 if not
            
            products.append(product)
        
        return products
    
    @staticmethod
    def get_test_product():
        return {
            'name': 'Test Product SMS',
            'points': 1000,
            'url': 'https://example.com/test-product',
            'available': True,
            'image_url': 'https://example.com/test-product-image.jpg',
            'link_url': 'https://example.com/test-product',
            'description': 'This is a test product to trigger SMS notification',
            'stock': 5
        }