from rest_framework.serializers import ModelSerializer, ListField

from .models import ClientOrder, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True, allow_empty=False)

    class Meta:
        model = ClientOrder
        fields = ['products', 'firstname', 'lastname', 'phonenumber', 'address']

# print(repr(OrderSerializer()))


