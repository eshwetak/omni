from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from products.models import Vendors, Products
from django.db import connection

from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.
class APIResponse:
    @staticmethod
    def send(data, code=status.HTTP_200_OK, error=None):
        if error:
            return Response(data=error, status=code)
        return Response(data=data, status=code)

class VendorsController(APIView):
    @staticmethod
    def get(request):
        query_dict = request.GET
        lat = query_dict.get('lat')
        lon = query_dict.get('lon')
        sample = query_dict.get('sample_delivery')
        virtual = query_dict.get('virtual_assistance')

        stores = Vendors.objects.all()

        if "sample_delivery" in query_dict:
            stores = stores.filter(sample_delivery=sample)
        if "virtual_assistance" in query_dict:
            stores = stores.filter(virtual_assistance=virtual)
        stores = stores.values()

        if lat and lon:
            for i in stores:
                x0, y0 = float(lat), float(lon)
                x1, y1 = float(i['latitude']), float(i['longitude'])
                d = (x1 - x0)**2 + (y1 - y0)**2
                i['distance'] = d
            stores = sorted(stores, key=lambda i : i['distance'])

        return APIResponse.send({'stores': stores})
    
class ProductsController(APIView):
    @staticmethod
    def get(request):
        query_dict = request.GET
        ven_id = query_dict.get('vendor_id')
        query = f'''SELECT  products.image,
                            products.display_name as product_display_name,
                            products.is_liked,
                            vendors.display_name as vendor_display_name,
                            price.amount,
                            price.currency
                    from products
                    inner join vendors on vendors.id = products.vendor_id
                    left join price on products.id = price.product_id
                    where price.vendor_id = {ven_id} and products.vendor_id = {ven_id};'''
        
        with connection.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
        colms = [i[0] for  i in cur.description]

        response = [dict(zip(colms, row)) for row in rows]
        return APIResponse.send({'products': response})
