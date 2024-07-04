import requests

class MeoService:
    BASE_HEADERS = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt-US;q=0.7,pt;q=0.6,nl;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    @classmethod
    def get_store_products(cls):
        url = 'https://app-9015f501-af0b-463a-b954-ab7059b01626.apps.meo.pt/api/v3StoreFront/GetStoreFrontProducts'
        headers = cls.BASE_HEADERS.copy()
        headers.update({
            'Content-Type': 'application/json',
            'Origin': 'https://loja.meo.pt',
            'Referer': 'https://loja.meo.pt/',
        })
        payload = {
            'Refiners': [],
            'Sorting': 'Other',
            'PathName': '/Equipamentos/sensacoes'
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json() if response.status_code == 200 else None

    @classmethod
    def get_points_balance(cls):
        url = "https://cliente.meo.pt/api/PointsMember/GetPointsBalance"
        headers = cls.BASE_HEADERS.copy()
        headers.update({
            'Content-Length': '678',
            'Content-Type': 'application/json; charset=UTF-8',
            'Origin': 'https://cliente.meo.pt',
            'Referer': 'https://cliente.meo.pt/home-pacote-telemovel-pospago',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-chua-platform': '"Windows"',
        })
        payload = {
            "Header": {
                "ID": "9f165a8a-17b4-b0a4-5dae-3f0360bdd86d",
                "WidgetID": "4653ffe7-0482-4b71-8005-b0f483dafed5",
                "Widdst": "MDNQU0cyOFg5bktnMVdsM1VwWFlOUWNHSkZheHo0TVJMSlgyRkF2a3N5Z2s2NGRtS1h1a0lHK1NHSTV1M2syVUg0MU9Pb1Axc1drd3VDbFdESTBqckJMU1Nla1Q2MmN2d0RETDl4NFRxSmREMHVVVEdNUVNUcmxHYWtzeEFXd3JXVmp6ZGRreUtpSmdtTlJYRGthUFBpU20yOTBqcmJJS2JlN280MU1nSE4zSmNoc1g5ZEhPeGdXYmJ3RGZDdHY2Wmxhb3dKS3M3MElOTVNrVVN4L3FDbTZVR3U5NDNHakRUUUp4NGZMSGprSHJDV05CNnNQc1FRL0x6YmFyVjE2UlZxNFNCTDRraXVRejlTWGxPYlJ1OXVWWmo0ekhpUzNxWDJlOHhtenNpMnlVcGFQTkdxOEsweXdHMzE1KzlIbTR0QVc0Q2pMWWJzSHI2NTBPYi9WYnVMTmpoV3hBL3VNRHArdE1IOHVNKzR5OTRvKzFCak02T3E4SEU4SitmQXMrVDQ="
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json() if response.status_code == 200 else None