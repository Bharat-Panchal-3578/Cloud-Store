import pytest
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem
from products.models import Product
from cart.services import add_to_cart

User = get_user_model()

@pytest.mark.django_db
class TestOrderViews:
    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', email="test@example.com", password='testpassword123')
        self.other_user = User.objects.create_user(username='otheruser', email="other@example.com", password='otherpassword123')
        self.product = Product.objects.create(name="Test Product", slug="test-product", price=Decimal("15.00"), is_active=True)
    
    def test_order_list_view_requires_login(self, client):
        response = client.get(reverse('order_list'))

        assert response.status_code == 302
    
    def test_order_list_view_shows_only_user_orders(self, client):
        order = Order.objects.create(user=self.user, total_amount=Decimal("15.00"), status="PENDING")
        other_order = Order.objects.create(user=self.other_user, total_amount=Decimal("30.00"), status="PENDING")

        client.force_login(user=self.user)
        response = client.get(reverse('order_list'))
        orders = response.context['orders']

        assert list(orders) == [order]
    
    def test_order_detail_view_only_accessible_to_owner(self, client):
        order = Order.objects.create(user=self.user, total_amount=Decimal("15.00"), status="PENDING")

        client.force_login(user=self.other_user)
        response = client.get(reverse('order_detail', args=[order.id]))

        assert response.status_code == 404
    
    def test_order_detail_view_shows_items(self, client):
        order = Order.objects.create(user=self.user, total_amount=Decimal("30.00"), status="PENDING")
        OrderItem.objects.create(order=order, product=self.product, quantity=2, price_at_purchase=Decimal("15.00"))

        client.force_login(user=self.user)
        response = client.get(reverse('order_detail', args=[order.id]))
        items = response.context['items']

        assert response.status_code == 200
        assert len(items) == 1
        assert items[0]['product'] == self.product
        assert items[0]['quantity'] == 2
        assert items[0]['price_at_purchase'] == Decimal("15.00")
        assert items[0]['subtotal'] == Decimal("30.00")
    
    def test_checkout_view_creates_order(self, client):
        client.force_login(user=self.user)

        session = client.session
        session['cart'] = {str(self.product.id): {'quantity': 2}}
        session.save()

        response = client.post(reverse('checkout'))

        order = Order.objects.first()
        items = order.items.all()

        assert response.status_code == 302
        assert order.total_amount == Decimal("30.00")
        assert order.status == "PENDING"
        assert len(items) == 1
        assert items[0].product == self.product
        assert items[0].quantity == 2
        assert items[0].price_at_purchase == Decimal("15.00")
    
    def test_checkout_view_empty_cart_redirects(self, client):
        client.force_login(user=self.user)

        response = client.post(reverse('checkout'))

        assert response.status_code == 302
        assert response.url == reverse('cart_detail')