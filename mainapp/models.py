from django.db import models


# Create your models here

class Categories(models.Model):
    name_category = models.CharField(verbose_name='Название категории', max_length=128, unique=True)
    header_category = models.CharField(verbose_name='Заголовок категории', max_length=128, blank=True)
    description_category = models.TextField(verbose_name='Описание категории', blank=True)
    show_in_main_menu = models.BooleanField(verbose_name='Выводить страницу в главном меню?', default=False)
    is_active = models.BooleanField(db_index=True, verbose_name='Показывать категорию', default=True)

    def __str__(self):
        return self.name_category

    class Meta:
        verbose_name_plural = 'Категории товаров'
        verbose_name = 'Категория'
        ordering = ['is_active', 'name_category']


class Products(models.Model):
    name_product = models.CharField(verbose_name='Название товара', max_length=128)
    description_product = models.TextField(verbose_name='Описание товара', blank=True)
    # предварительно pip install pillow
    image_product = models.ImageField(upload_to='images_products', blank=True, default='images_products/no_image.jpg')
    quantity = models.PositiveIntegerField(verbose_name='Кол-во на складе', null=False, default=10)
    price_product = models.PositiveIntegerField(verbose_name='Цена товара', null=False)  # цена больше 0 и без копеек
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    is_new = models.BooleanField(db_index=True, verbose_name='Новый товар', default=False)
    is_discount = models.BooleanField(db_index=True, verbose_name='Товар со скидкой', default=False)
    is_popular = models.BooleanField(db_index=True, verbose_name='Популярный товар', default=False)
    is_exclusive = models.BooleanField(db_index=True, verbose_name='Эксклюзивный товар', default=False)
    is_active = models.BooleanField(db_index=True, verbose_name='Показывать товар', default=True)

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ['is_active', 'name_product']

    def __str__(self):
        return self.name_product

    @staticmethod
    def get_items():
        return Products.objects.filter(is_active=True).order_by('category', 'name_product')


class InfoPages(models.Model):
    name_page = models.CharField(verbose_name='Название страницы', max_length=128, unique=True)
    header_page = models.CharField(verbose_name='Заголовок страницы', max_length=128, blank=True)
    content_page = models.TextField(verbose_name='Контент страницы', blank=True, default='<p></p>')
    show_in_main_menu = models.BooleanField(db_index=True, verbose_name='Выводить страницу в главном меню?', default=False)
    order_in_menu = models.PositiveIntegerField(verbose_name='Номер в меню', default=0)

    class Meta:
        verbose_name_plural = 'Информационные страницы'
        verbose_name = 'Инфостраница'
        ordering = ['name_page']

    def __str__(self):
        return self.name_page
