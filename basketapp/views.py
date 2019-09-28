from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models import F

from mainapp.models import Products
from basketapp.models import Basket
from mainapp.views import main_menu, footer_menu, get_basket


# Create your views here.
@login_required
def index(request):
    content = {
        'title': 'Корзина',
        'header1_page': 'Корзина товаров',
        'main_menu': main_menu(),
        'info_pages': footer_menu(),
        'basket': get_basket(request),
    }
    return render(request, 'basketapp/index.html', content)


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('main:product', kwargs={'pk': pk}))
    product = get_object_or_404(Products, pk=pk)
    basket_item = Basket.objects.filter(user=request.user, product=product).first()
    if basket_item:
        basket_item.quantity = F('quantity') + 1
        basket_item.save()
    else:
        Basket.objects.create(user=request.user, product=product, quantity=1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_delete(request, pk):
    get_object_or_404(Basket, pk=pk).delete()
    # вернуться туда, откуда мы пришли
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_update(request, pk, quantity):
    if request.is_ajax():
        basket_obj = get_object_or_404(Basket, pk=pk)
        quantity = int(quantity)
        if quantity > 0:
            basket_obj.quantity = quantity
            basket_obj.save()
        else:
            basket_obj.delete()
        content = {
            'title': 'Корзина',
            'header1': 'Корзина',
            'main_menu': main_menu(),
            'info_pages': footer_menu(),
            'basket': get_basket(request),
        }
        result = render_to_string('basketapp/includes/inc__basket_list.html', content)
        return JsonResponse({
            'result': result,
        })
