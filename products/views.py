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

def queryDb(query):
    with connection.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        colms = [i[0] for  i in cur.description]
    response = [dict(zip(colms, row)) for row in rows]
    return response

class VendorsController(APIView):
    @staticmethod
    def get(request):
        query_dict = request.GET
        lat = query_dict.get('lat')
        lon = query_dict.get('lon')

        stores = Vendors.objects.all()
        if "sample_delivery" in query_dict:
            stores = stores.filter(sample_delivery=query_dict['sample_delivery'])
        if "virtual_assistance" in query_dict:
            stores = stores.filter(virtual_assistance=query_dict['virtual_assistance'])
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

        return JsonResponse({'products': queryDb(query)})

class ProductsController(APIView):
    @staticmethod
    def get(request):
        query_dict = request.GET
        
        if len(query_dict) > 0:
            condition = ' AND '.join(map(lambda i: f'{i[0]}={i[1]}', 
                                                query_dict.items()))
            condition = 'where ' + condition
        else: condition = ''
       
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

        return JsonResponse({'products': queryDb(query)})

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
                        products.cart_item_count,
                        products.description,
                        products.dimension
                    from products
                    inner join vendors on vendors.id = products.vendor_id
                    WHERE products.id = {id};'''

        response = queryDb(query)
        return JsonResponse(response and response[0])

    @staticmethod
    def put(request, id):
        data=request.data
        allowed_keys = ['in_cart', 'cart_item_count', 'is_liked']

        product = Products.objects.get(pk=id)
        for key in allowed_keys:
            if key in data.keys():
                setattr(product, key, data[key])
        product.save()

        p = product.__dict__
        p.pop('_state')
        p['product_display_name'] = p.pop('display_name')

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
        
        response = queryDb(query)
        return JsonResponse(response and response[0])

class SimilarProducts(APIView):
    @staticmethod
    def get(request, criteria):
        query = f'''SELECT  products.id,
                        products.image,
                        products.display_name as product_display_name,
                        products.is_liked,
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
                    WHERE  color LIKE '%{criteria}%' or 
                            kind like '%{criteria}%' or 
                            prices like '%{criteria}%' or 
                            style like '%{criteria}%';'''
        
        return JsonResponse({'products': queryDb(query)})


# class GenerateQrCode(APIView):
#     @staticmethod
#     def get(request):
#         query_dict = request.GET
#         prodt_name = query_dict.get('product_name')
#         ven_name = query_dict.get('vendor_name')

#         qrStr = 'asdf'
#         url = QRCode(content=b'836590873213', error='H', version=3, mode='binary')
#         url.show()
            # return JsonResponse({'status': 200})
