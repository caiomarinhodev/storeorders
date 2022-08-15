from rest_framework import serializers

from app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "client_name", "status", "total_value")
