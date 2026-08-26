from django.test import TestCase
from .models import Category, Product

class RestaurantModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Desserts", slug="desserts")
        self.product = Product.objects.create(
            category=self.category,
            name="Ice Cream",
            price=100,
            is_available=True
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Desserts")

    def test_product_str(self):
        self.assertEqual(str(self.product), "Ice Cream")

class RestaurantViewTests(TestCase):
    def test_menu_view_status_code(self):
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
