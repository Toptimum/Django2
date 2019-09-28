from django.db import models
from django.conf import settings

from mainapp.models import Products


# Create your models here.

class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'заказ формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'заказ оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'заказ отменен'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Заказ создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Заказ обновлен', auto_now=True)
    status = models.CharField(verbose_name='Статус заказа', max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    class Meta:
        ordering = ('-created',)  # сортировка по умолчанию от более новых к старым заказам
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Текущий заказ: {}'.format(self.id)

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    # def get_total_quantity(self):
    #     items = self.orderitems.select_related()
    #     return sum(list(map(lambda x: x.quantity, items)))
    #
    # def get_total_cost(self):
    #     items = self.orderitems.select_related()
    #     return sum(list(map(lambda x: x.quantity * x.product.price_product, items)))

    # Вместо двух методов get_total_quantity() и get_total_cost() создадим один get_summary(), возвращающий словарь:
    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price_product, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }

    # переопределяем метод, удаляющий объект
    def delete(self):
        for item in self.orderitems.select_related():  # находим все элементы заказа
            item.product.quantity += item.quantity  # корректируем остатки продуктов на складе
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    # Доступ к элементам заказа через атрибут orderitems возможен благодаря аргументу related_name
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name='продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.product.price_product * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()
