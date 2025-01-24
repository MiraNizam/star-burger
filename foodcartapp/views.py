import json

from django.http import JsonResponse
from django.templatetags.static import static
from django.shortcuts import get_object_or_404


from .models import Product, ClientOrder, OrderItem


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


def register_order(request):
    try:
        order_form = json.loads(request.body.decode())
    except ValueError:
        return JsonResponse({
            'error': 'Что-то пошло не так',
        })
    new_order = ClientOrder.objects.create(
        firstname=order_form['firstname'],
        lastname=order_form['lastname'],
        phonenumber=order_form['phonenumber'],
        address=order_form['address']
    )

    for product in order_form['products']:
        OrderItem.objects.create(
            order=new_order,
            product=get_object_or_404(Product, id=product['product']),
            quantity=product['quantity']
        )
    return JsonResponse(order_form)

