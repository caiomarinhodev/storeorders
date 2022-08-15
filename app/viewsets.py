from rest_framework import viewsets

from django_filters import rest_framework as filters

from . import (
    serializers,
    models
)

import django_filters


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = models.Order
        fields = ["id", "client_name", "status__name", "total_value"]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter
