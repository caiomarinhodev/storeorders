from django.urls import path

from app import conf
from app.views.account import LoginView, RegisterView, LogoutView

urlpatterns = []

from app.views import order

urlpatterns += [
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),
    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),
    # order
    path(
        '',
        order.List.as_view(),
        name=conf.ORDER_LIST_URL_NAME
    ),
    path(
        'order/create/',
        order.Create.as_view(),
        name=conf.ORDER_CREATE_URL_NAME
    ),
    path(
        'order/<int:pk>/',
        order.Detail.as_view(),
        name=conf.ORDER_DETAIL_URL_NAME
    ),
    path(
        'order/<int:pk>/update/',
        order.Update.as_view(),
        name=conf.ORDER_UPDATE_URL_NAME
    ),
    path(
        'order/<int:pk>/delete/',
        order.Delete.as_view(),
        name=conf.ORDER_DELETE_URL_NAME
    )
]
