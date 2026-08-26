from django.test import TestCase

class OrdersViewTests(TestCase):
    def test_cart_view_status_code(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')
