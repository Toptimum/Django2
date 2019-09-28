from django.test import TestCase
from django.test.client import Client
from mainapp.models import Categories, Products
from django.core.management import call_command

# Create your tests here.
print("Тестирование работоспособности страниц")


# Все тесты создаются в виде классов-потомков TestCase
class TestMainappSmoke(TestCase):
    # Прописываем код подготовки к тестам
    def setUp(self):
        call_command('flush', '--noinput')
        # очищаем базу и импортируем данные при помощи функции
        call_command('loaddata', 'test_db_mainapp.json')
        # создаем объект класса Client для отправки запросов
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        for category in Categories.objects.all():
            response = self.client.get(f'/category/{category.pk}/')
            self.assertEqual(response.status_code, 200)

        for product in Products.objects.all():
            response = self.client.get(f'/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)

    # разные базы данных по-разному работают с индексами при создании новых элементов - добавили метод
    # выполняющийся всегда по завершении тестов в классе, команду сброса индексов
    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
