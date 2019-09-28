from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from mainapp.models import Products


# Create your models here.

class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__category')

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    @property
    def product_cost(self):
        # "return cost of all products this type"
        return self.product.price_product * self.quantity

    # @property
    # def total_quantity(self):
    #     # "return total quantity for user"
    #     # берем все, что есть в корзине
    #     # и для каждого элемента берем его кол-во и суммируем
    #     return sum([el.quantity for el in self.user.basket.all()])
    #
    # @property
    # def total_cost(self):
    #     # "return total cost for user"
    #     return sum([el.product_cost for el in self.user.basket.all()])

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    def get_total_quantity(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    def get_total_cost(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.product_cost, _items)))
