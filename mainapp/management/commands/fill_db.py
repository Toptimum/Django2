import json
import os
from django.core.management.base import BaseCommand  # импортируем стандартный класс для команд
from mainapp.models import Categories, Products  # импортируем наши модели Категорий и Товаров
# from django.contrib.auth.models import User  # подгружаем стандартную модель пользователя (User)
from authapp.models import ShopUser

JSON_PATH = 'mainapp/json'


# функция считывания данных из файла json
def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as file_obj:
        return json.load(file_obj)


class Command(BaseCommand):  # нашу команду наследуем от стандартного класса команд
    def handle(self, *args, **options):  # метод handle автоматически вызывается при вызове команды в консоли

        # сначала загружаем данные Категорий из файла
        categories = load_from_json('mainapp_categories')
        Categories.objects.all().delete()  # удаляем данные из базы, чтобы избежать дубликатов
        for category in categories:
            Categories.objects.create(**category)  # второй вариант созданий объекта в базе

        # затем можно работать с товарами
        products = load_from_json('mainapp_products')
        Products.objects.all().delete()
        for product in products:
            # name_category относится к Categories, а product['category'] к Products
            product['category'] = Categories.objects.get(name_category=product['category'])
            Products.objects.create(**product)

            # Прежняя команда работала: Создаем суперпользователя при помощи менеджера модели
            # if not User.objects.filter(username='django').exists():  # если пользователя нет, тогда создаем его
            #      User.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains')
        if not ShopUser.objects.filter(username='django').exists():  # если пользователя нет, тогда создаем его
            ShopUser.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains', age=31)
