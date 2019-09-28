from django.test import TestCase

from mainapp.models import Categories, Products


class ProductsTestCase(TestCase):
    def setUp(self):
        category = Categories.objects.create(name_category="стулья")
        self.product_1 = Products.objects.create(name_product="стул 1", category=category, price_product=1999,
                                                 quantity=150)
        self.product_2 = Products.objects.create(name_product="стул 2", category=category, price_product=2998,
                                                 quantity=125,
                                                 is_active=False)
        self.product_3 = Products.objects.create(name_product="стул 3", category=category, price_product=998,
                                                 quantity=115)

    def test_product_get(self):
        product_1 = Products.objects.get(name_product="стул 1")
        product_2 = Products.objects.get(name_product="стул 2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Products.objects.get(name_product="стул 1")
        product_2 = Products.objects.get(name_product="стул 2")
        self.assertEqual(str(product_1), 'стул 1')
        self.assertEqual(str(product_2), 'стул 2')

    def test_product_get_items(self):
        product_1 = Products.objects.get(name_product="стул 1")
        product_3 = Products.objects.get(name_product="стул 3")
        products = product_1.get_items()
        self.assertEqual(list(products), [product_1, product_3])
