from rest_framework.routers import DefaultRouter
from app import (
    viewsets
)

api_urlpatterns = []

order_router = DefaultRouter()

order_router.register(
    r'^api/order',
    viewsets.OrderViewSet,
    basename="order"
)

api_urlpatterns += order_router.urls
