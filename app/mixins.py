from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import FieldDoesNotExist, PermissionDenied

from app.models import Order
from app.request_api import get_order


class Unauthorized(Exception):
    """The user did not have permission to do that"""
    pass


class OrderMixin(object):

    def get(self, request, *args, **kwargs):
        try:
            return super(OrderMixin, self).get(request, *args, **kwargs)
        except (Unauthorized,):
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def get_token(self):
        return self.request.user.token_set.last().token

    def get_context_data(self, **kwargs):
        context = super(OrderMixin, self).get_context_data(**kwargs)
        return context

    def get_order(self):
        return get_order(self.get_token(), self.kwargs.get('pk'))
