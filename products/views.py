from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from products.models import Vendors, Products
from django.db import connection
# import pyqrcode
# import png
# from pyqrcode import QRCode
from django.http import JsonResponse

qrcodes = {
    1: 836590873213,
    2: 678532790765,
    3: 746499766876
}

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

        return JsonResponse({'stores': list(stores)})
    
class ProductsController(APIView):
    @staticmethod
    def get(request, id):
        query_dict = request.GET
        query = f'''SELECT  products.image,
                            products.display_name as product_display_name,
                            products.is_liked,
                            vendors.display_name as vendor_display_name,
                            products.prices
                    from products
                    inner join vendors on vendors.id = products.vendor_id
                    where products.vendor_id = {id};'''
        
        with connection.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
        colms = [i[0] for  i in cur.description]

        response = [dict(zip(colms, row)) for row in rows]
        return JsonResponse({'products': response})

class ProductDetails(APIView):
    @staticmethod
    def get(request, id):
        query = f'''SELECT  products.image,
                        products.display_name as product_display_name,
                        products.is_liked,
                        vendors.display_name as vendor_display_name,
                        products.prices,
                        products.color,
                        products.sku,
                        products.description,
                        products.dimension
                    from products
                    inner join vendors on vendors.id = products.vendor_id
                    WHERE products.id = {id};'''

        with connection.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
        colms = [i[0] for  i in cur.description]
        response = [dict(zip(colms, row)) for row in rows]
        return JsonResponse(response and response[0])


class FetchVendorById(APIView):
    @staticmethod
    def get(request, id):
        query = f'''SELECT  vendors.image,
                        vendors.display_name,
                        vendors.ratings,
                        vendors.address,
                        vendors.open_slot,
                        vendors.sample_delivery,
                        vendors.virtual_assistance,
                        vendors.store_kind
                    from vendors
                    where vendors.id ={id};'''
        
        with connection.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
        colms = [i[0] for  i in cur.description]
        response = [dict(zip(colms, row)) for row in rows]
        return JsonResponse(response and response[0])

# class GenerateQrCode(APIView):
#     @staticmethod
#     def get(request):
#         query_dict = request.GET
#         prodt_name = query_dict.get('product_name')
#         ven_name = query_dict.get('vendor_name')

#         qrStr = "asdf"
#         url = QRCode(content=b'836590873213', error='H', version=3, mode='binary')
#         url.show()
#         return APIResponse.send()
