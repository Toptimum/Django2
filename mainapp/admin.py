from django.contrib import admin

from .models import Categories, Products, InfoPages


# Register your models here

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name_category', 'header_category', 'is_active')
    list_display_links = ('is_active', 'name_category', 'header_category')
    search_fields = ('name_category', 'header_category', 'description_category')


admin.site.register(Categories, CategoriesAdmin)


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'name_product', 'price_product', 'category', 'is_new', 'is_discount',
                    'is_popular', 'is_exclusive')
    list_display_links = ('is_active', 'name_product')
    search_fields = ('name_product', 'description_product')


admin.site.register(Products, ProductsAdmin)


class InfoPagesAdmin(admin.ModelAdmin):
    list_display = ('name_page', 'header_page', 'show_in_main_menu')
    list_display_links = ('name_page', 'header_page')
    search_fields = ('name_page', 'header_page', 'content_page')


admin.site.register(InfoPages, InfoPagesAdmin)
