from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import ClientOrder, OrderItem

# Валидация + Нормализация = Десериализация. все чтобы данные были проверены, исправлены для залития в бд
class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product',
                  'quantity'
                  ]


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True, allow_empty=False, write_only=True)

    class Meta:
        model = ClientOrder
        fields = ['id',
                  'products',
                  'firstname',
                  'lastname',
                  'phonenumber',
                  'address'
                  ]
