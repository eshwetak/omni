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
    836590873213: 1,
    678532790765: 2,
    746499766876: 3
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
    
class ProductsByVendor(APIView):
    @staticmethod
    def get(request, id):
        query = f'''SELECT  products.id,
                            products.image,
                            products.display_name as product_display_name,
                            products.is_liked,
                            vendors.display_name as vendor_display_name,
                            products.prices,
                            products.vendor_id
                    from products
                    inner join vendors on vendors.id = products.vendor_id
                    where products.vendor_id = {id};'''
        
        with connection.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
        colms = [i[0] for  i in cur.description]

        response = [dict(zip(colms, row)) for row in rows]
        return JsonResponse({'products': response})

class ProductsController(APIView):
    @staticmethod
    def get(request):
        query_dict = request.GET
        in_cart = query_dict.get('in_cart')
        is_liked = query_dict.get('is_liked')

        condition = f"where "
        if 'in_cart' in query_dict and 'is_liked' in query_dict:
            condition = f'''{condition} in_cart = {query_dict.get('in_cart')} and 
                            is_liked = {query_dict.get('is_liked')}'''
        elif 'in_cart' in query_dict:
            condition = f"{condition} in_cart = {query_dict.get('in_cart')}"
        elif 'is_liked' in query_dict:
            condition = f"{condition} is_liked = {query_dict.get('is_liked')}"

        query = f'''SELECT  products.id,
                        products.image,
                        products.display_name as product_display_name,
                        products.is_liked,
                        products.in_cart,
                        vendors.display_name as vendor_display_name,
                        products.vendor_id, 
                        products.prices,
                        products.cart_item_count,
                        products.color,
                        products.sku,
                        products.description,
                        products.dimension
                    from products
                    inner join vendors on vendors.id = products.vendor_id
                    {condition};'''
        
        with connection.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
        colms = [i[0] for  i in cur.description]
        response = [dict(zip(colms, row)) for row in rows]
        return JsonResponse({'products': response})

class ProductDetails(APIView):
    @staticmethod
    def get(request, id):
        codes = [836590873213, 678532790765, 746499766876]
        if id in codes:
            id = qrcodes[id]
        query = f'''SELECT  products.id,
                        products.image,
                        products.display_name as product_display_name,
                        products.is_liked,
                        vendors.display_name as vendor_display_name,
                        products.vendor_id, 
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

    @staticmethod
    def put(request, id):
        data=request.data
        product = Products.objects.get(pk=id)

        if 'in_cart' in data.keys():
            product.in_cart = data['in_cart']
        if 'cart_item_count' in data.keys():
            product.cart_item_count = data['cart_item_count']
        if 'is_liked' in data.keys():
            product.is_liked = data['is_liked']
        
        product.save()

        p = product.__dict__
        p.pop('_state')
        p['product_display_name'] = p['display_name']
        p.pop('display_name')

        return JsonResponse({'product': p})


class FetchVendorById(APIView):
    @staticmethod
    def get(request, id):
        query = f'''SELECT  vendors.id,
                        vendors.image,
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
