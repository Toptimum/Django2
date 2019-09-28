"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('category/<int:pk>/', mainapp.category, name='category'),
    path('category/<int:pk>/page/<int:page>/', mainapp.category, name='category_paginator'),
    path('product/<int:pk>/', mainapp.product, name='product'),
    path('infopage/<int:pk>/', cache_page(3600)(mainapp.infopage), name='infopage'),

    # re_path(r'^category/(?P<pk>\d+)/$', mainapp.category, name='category'),
    # re_path(r'^category/(?P<pk>\d+)/page/(?P<page>\d+)/$', mainapp.category, name='category_paginator'),
    # re_path(r'^product/(?P<pk>\d+)/$', mainapp.product, name='product'),
    # path('contacts/', mainapp.contacts, name='contacts'),
    # re_path(r'^infopage/(?P<pk>\d+)/$', mainapp.infopage, name='infopage'),
    # path('catalog/', mainapp.catalog, name='catalog'),
    # re_path(r'^catalog/(\d+)/$', mainapp.catalog, name='catalog'),
    # path('product/', mainapp.product, name='product'),
]
