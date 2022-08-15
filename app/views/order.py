#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, FormView
)
from django.views.generic.list import ListView

from app.request_api import get_orders, create_order, get_order, update_order, delete_order

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy, reverse

from app.models import Order
from app.forms import OrderForm
from app.mixins import OrderMixin
from app.conf import ORDER_DETAIL_URL_NAME


class List(LoginRequiredMixin, OrderMixin, ListView):
    """
    List all Orders
    """
    login_url = 'login/'
    template_name = 'order/list_full.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        res = get_orders(self.get_token())
        return res

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        page_size = self.get_paginate_by(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context.update(**{
                'ordering': self.ordering,
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset
            })
        else:
            context.update(**{
                'ordering': self.ordering,
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset
            })
        return context


class Create(LoginRequiredMixin, OrderMixin, FormView):
    """
    Create a Order
    """
    login_url = '/login/'
    form_class = OrderForm
    template_name = 'order/create.html'

    def get_success_url(self, response=None):
        return '/order/{}/'.format(response['id'])

    def form_valid(self, form):
        data = form.cleaned_data
        res = create_order(self.get_token(), data['client_name'], data['status'], data['total_value'], data['notes'])
        if res:
            messages.success(self.request, 'Pedido criado com sucesso')
            return HttpResponseRedirect(self.get_success_url(res))
        else:
            messages.error(self.request, 'Houve algum erro, tente novamente')
            return super(Create, self).form_invalid(form)


class Detail(LoginRequiredMixin, OrderMixin, TemplateView):
    """
    Detail of a Order
    """
    login_url = 'login/'
    template_name = 'order/detail.html'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        context['order'] = self.get_order()
        return context


class Update(LoginRequiredMixin, OrderMixin, FormView):
    """
    Update a Order
    """
    login_url = 'login/'
    template_name = 'order/update.html'
    form_class = OrderForm

    def get_initial(self):
        data = self.get_order()
        print(data)
        return data

    def get_success_url(self):
        return reverse_lazy(ORDER_DETAIL_URL_NAME, kwargs={'pk': self.kwargs.get("pk")})

    def get_context_data(self, **kwargs):
        data = super(Update, self).get_context_data(**kwargs)
        data['order'] = self.get_order()
        return data

    def form_valid(self, form):
        data = form.cleaned_data
        id_order = self.kwargs.get("pk")
        res = update_order(self.get_token(), id_order, data['client_name'], data['status'], data['total_value'],
                           data['notes'])
        if res:
            messages.success(self.request, 'Pedido atualizado com sucesso')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Houve algum erro, tente novamente')
            return super(Update, self).form_invalid(form)


class Delete(LoginRequiredMixin, OrderMixin, FormView):
    """
    Delete a Order
    """
    login_url = 'login/'
    template_name = 'order/delete.html'
    form_class = OrderForm

    def get_success_url(self):
        return '/'

    def get_context_data(self, **kwargs):
        data = super(Delete, self).get_context_data(**kwargs)
        data['order'] = self.get_order()
        return data

    def post(self, request, *args, **kwargs):
        id_order = self.kwargs.get("pk")
        form = self.get_form()
        res = delete_order(self.get_token(), id_order)
        if res:
            messages.success(self.request, 'Pedido excluído com sucesso')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Houve algum erro, tente novamente')
            return super(Delete, self).form_invalid(form)
