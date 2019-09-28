from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import F

from mainapp.models import Products
from basketapp.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm


# Create your views here.

class OrderList(ListView):
    model = Order

    # Переопределили метод get_queryset(), чтобы пользователь видел только свои заказы
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(ListView, self).dispatch(*args, **kwargs)


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    # необходимо передать набор форм в шаблон
    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            # Получаем объекты корзины пользователя
            basket_items = Basket.get_items(self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price_product
                basket_items.delete()
            else:  # Если корзина пустая - создаем набор с одной чистой формой
                formset = OrderFormSet()
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        # удаляем пустой заказ
        # if self.object.get_total_cost() == 0:
        total_cost = self.object.get_summary()
        if total_cost['total_cost'] == 0:
            self.object.delete()
        return super(OrderItemsCreate, self).form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(CreateView, self).dispatch(*args, **kwargs)


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(DetailView, self).dispatch(*args, **kwargs)


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            # data['orderitems'] = OrderFormSet(instance=self.object)
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price_product
            data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        # удаляем пустой заказ
        # if self.object.get_total_cost() == 0:
        total_cost = self.object.get_summary()
        if total_cost['total_cost'] == 0:
            self.object.delete()
        return super(OrderItemsUpdate, self).form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)


def get_product_price(request, pk):
    if request.is_ajax():
        product = Products.objects.filter(pk=int(pk)).first()
        if product:
            return JsonResponse({'price': product.price_product})
        else:
            return JsonResponse({'price': 0})


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(DeleteView, self).dispatch(*args, **kwargs)


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'product':
        # Проверяем, новый это объект или уже существующий
        if instance.pk:
            instance.product.quantity -= F('quantity') - sender.get_item(instance.pk).quantity
        else:
            instance.product.quantity = F('quantity') - 1
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity = F('quantity') + 1
    instance.product.save()
