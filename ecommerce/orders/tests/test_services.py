import pytest
from decimal import Decimal
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from orders.services import create_order_from_cart
from orders.models import Order, OrderItem
from products.models import Product
from cart.services import add_to_cart, CART_SESSION_KEY

User = get_user_model()

@pytest.mark.django_db
class TestOrderServices:
    def setup_method(self):
        self.factory = RequestFactory()
        self.request = self.factory.post('/orders/checkout/')

        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(self.request)
        self.request.session.save()

        self.user = User.objects.create_user(username='testuser', email="test@example.com",password='testpassword123')

        self.product1 = Product.objects.create(name="Product 1", slug="product-1", price=Decimal("10.00"), is_active=True)
        self.product2 = Product.objects.create(name="Product 2", slug="product-2", price=Decimal("20.00"), is_active=True)

    def test_creat_order_from_cart_success(self):
        add_to_cart(self.request, self.product1.id, 2)
        add_to_cart(self.request, self.product2.id, 1)

        order = create_order_from_cart(self.request, self.user)
        items = order.items.all()
        quantities = {item.product.id: item.quantity for item in items}

        assert Order.objects.count() == 1
        assert OrderItem.objects.count() == 2
        assert order.user == self.user
        assert order.total_amount == Decimal("40.00")
        assert order.status == "PENDING"
        assert quantities[self.product1.id] == 2
        assert quantities[self.product2.id] == 1
        assert CART_SESSION_KEY not in self.request.session

        for item in items:
            assert item.price_at_purchase == item.product.price
    
    def test_create_order_from_cart_empty_cart(self):
        with pytest.raises(ValueError):
            create_order_from_cart(self.request, self.user)

        assert Order.objects.count() == 0
        assert OrderItem.objects.count() == 0