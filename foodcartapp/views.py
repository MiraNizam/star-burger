import json

from django.http import JsonResponse
from django.templatetags.static import static
from django.shortcuts import get_object_or_404


from .models import Product, ClientOrder, OrderItem

from rest_framework.decorators import api_view
from rest_framework.response import Response

def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    order_form = request.data
    if 'products' not in order_form:
        return Response({"error": "product key not presented"}, status=400)
    if not isinstance(order_form['products'], list):
        return Response({"error": "product key not presented or not list"}, status=400)
    if len(order_form['products']) == 0:
        return Response({"error": "products:  field cannot be empty."}, status=400)

    # serializer = ModelSerializer(data=order_form)
    # if serializer.is_valid():
    #     serializer.save()
    return Response(order_form, status=201)
    # else:
    #     return Response(serializer.errors, status=400)
    # try:
    #     order_form = json.loads(request.body.decode())
    # except ValueError:
    #     return JsonResponse({
    #         'error': 'Что-то пошло не так',
    #     })
    # new_order = ClientOrder.objects.create(
    #     firstname=order_form['firstname'],
    #     lastname=order_form['lastname'],
    #     phonenumber=order_form['phonenumber'],
    #     address=order_form['address']
    # )
    #
    # for product in order_form['products']:
    #     OrderItem.objects.create(
    #         order=new_order,
    #         product=get_object_or_404(Product, id=product['product']),
    #         quantity=product['quantity']
    #     )

# {"products": [{"product": 2, "quantity": 1}, {"product": 3, "quantity": 1}], "firstname": "ELMIRA", "lastname": "NIZAMOVA", "phonenumber": "89657859158", "address": "Sankt-Peterburg"}


