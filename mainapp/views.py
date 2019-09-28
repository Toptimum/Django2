import random
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from itertools import chain

from .models import Categories, Products, InfoPages


# Create your views here

# main_menu = [
#     {'href': 'category/1/', 'name': 'Смартфоны'},
#     {'href': '#', 'name': 'Оплата'},
#     {'href': '#', 'name': 'Доставка'},
#     {'href': 'contacts', 'name': 'Контакты'}
# ]

# def main_menu():
#     categories = Categories.objects.filter(show_in_main_menu=True)
#     info_pages = InfoPages.objects.filter(show_in_main_menu=True)
#     main_menu = list(chain(categories, info_pages.order_by('order_in_menu')))
#     return main_menu

def main_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            categories = Categories.objects.filter(show_in_main_menu=True)
            info_pages = InfoPages.objects.filter(show_in_main_menu=True)
            links_menu = list(chain(categories, info_pages.order_by('order_in_menu')))
            cache.set(key, links_menu)
        return links_menu
    else:
        categories = Categories.objects.filter(show_in_main_menu=True)
        info_pages = InfoPages.objects.filter(show_in_main_menu=True)
        links_menu = list(chain(categories, info_pages.order_by('order_in_menu')))
        return links_menu


# def footer_menu():
# #     info_pages = InfoPages.objects.all()
# #     return info_pages

def footer_menu():
    if settings.LOW_CACHE:
        key = 'links_footer_menu'
        links_footer_menu = cache.get(key)
        if links_footer_menu is None:
            links_footer_menu = info_pages = InfoPages.objects.all()
            cache.set(key, links_footer_menu)
        return links_footer_menu
    else:
        return InfoPages.objects.all()


# def get_categories():  # получаем все объекты категорий
#     return Categories.objects.filter(is_active=True)

def get_categories():
    if settings.LOW_CACHE:
        key = 'links_categories'
        links_categories = cache.get(key)
        if links_categories is None:
            links_categories = Categories.objects.filter(is_active=True)
            cache.set(key, links_categories)
        return links_categories
    else:
        return Categories.objects.filter(is_active=True)


# def get_products():  # получаем все объекты товаров
#     return Products.objects.filter(is_active=True)

def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Products.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Products.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_basket(request):
    if request.user.is_authenticated:
        return request.user.basket.all().order_by('product__category')  # из юзера достаем корзину
    else:
        return []


def get_hot_product(request):
    return random.choice(Products.objects.all())


def main(request):
    new_products = Products.objects.filter(is_active=True, is_new=True)
    popular_products = Products.objects.filter(is_active=True, is_popular=True)
    exclusive_products = Products.objects.filter(is_active=True, is_exclusive=True)

    content = {
        'title': 'Главная страница магазина',
        'main_menu': main_menu,
        'info_pages': footer_menu(),
        'products': get_products(),
        'new_products': new_products,
        'popular_products': popular_products,
        'exclusive_products': exclusive_products,
    }
    return render(request, 'mainapp/index.html', context=content)


# def catalog(request):
#     content = {
#         'title': 'Каталог товаров',
#         'header1': 'Как определять категорию? Чтобы загружать соответствующие заголовки и товары.',
#         'main_menu': main_menu,
#         'categories': get_categories(),
#         'products': get_products()
#     }
#     return render(request, 'mainapp/catalog.html', content)

def category(request, pk, page=1):
    pk = int(pk)
    if pk == 1:  # если категория (Все модели с pk = 1), то выводим все товары
        current_category = Categories.objects.get(pk=1)
        # current_category = get_object_or_404(Categories, pk=1)
        products_category = Products.objects.filter(is_active=True)
    else:  # по primary key выводим товары этой категории
        current_category = Categories.objects.filter(pk=pk).first()
        products_category = Products.objects.filter(category=pk, is_active=True)

    paginator = Paginator(products_category, 15)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    content = {
        'title': current_category.header_category,
        'header1': current_category.header_category,
        'main_menu': main_menu(),
        'info_pages': footer_menu(),
        'categories': get_categories(),
        'category': current_category,
        'products': products_paginator,
    }
    return render(request, 'mainapp/catalog.html', content)


def product(request, pk):
    product = Products.objects.get(pk=pk, is_active=True)
    # выбираем похожие товары по категории, исключая текущий товар
    same_products = Products.objects.filter(category=product.category, is_active=True).exclude(pk=pk)
    content = {
        'title': product.name_product,
        'header1': product.name_product,
        'product': product,
        'same_products': same_products,
        'main_menu': main_menu(),
        'info_pages': footer_menu(),
        'categories': get_categories(),
        'products': get_products(),
    }
    return render(request, 'mainapp/product.html', context=content)


def contacts(request):
    content = {
        'title': 'Контакты интернет-магазина MyPhone',
        'header1': 'Контакты магазина',
        'main_menu': main_menu(),
        'info_pages': footer_menu(),
    }
    return render(request, 'mainapp/contacts.html', context=content)


def infopage(request, pk):
    current_page = InfoPages.objects.filter(pk=pk).first()
    content = {
        'page': current_page,
        'title': current_page.header_page,
        'main_menu': main_menu(),
        'info_pages': footer_menu(),
    }
    return render(request, 'mainapp/infopage.html', context=content)
