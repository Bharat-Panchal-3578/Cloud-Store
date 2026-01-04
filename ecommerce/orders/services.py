from decimal import Decimal
from django.db import transaction
from orders.models import Order, OrderItem
from products.models import Product
from cart.services import get_cart_items, CART_SESSION_KEY

def _get_cart_items(request):
    """
    Fetch cart items for the current session/user.
    """
    return get_cart_items(request)

def _calculate_total(cart_items):
    """
    Calculate the total amount for the cart items.
    """
    total = Decimal("0.00")
    for item in cart_items:
        total += item["total_price"]
    return total

def _create_order(user, total_amount):
    """
    Create order instance
    """
    return Order.objects.create(
        user=user,
        total_amount=total_amount,
        status="PENDING",
    )
    

def _create_order_items(order, cart_items):
    """
    Create OrderItem instances for the order
    """
    order_items = []
    for item in cart_items:
        order_item = OrderItem(
            order=order,
            product=item["product"],
            quantity=item["quantity"],
            price_at_purchase=item["product"].price,
        )
        order_items.append(order_item)
    OrderItem.objects.bulk_create(order_items)

def _clear_cart(request):
    """
    Clear cart from session.
    """
    if CART_SESSION_KEY in request.session:
        del request.session[CART_SESSION_KEY]
        request.session.modified = True

@transaction.atomic
def create_order_from_cart(request, user):
    """
    Create an order from the current cart items.
    """
    cart_items = _get_cart_items(request)

    if not cart_items:
        raise ValueError("Cart is empty")

    total_amount = _calculate_total(cart_items)
    order = _create_order(user, total_amount)
    _create_order_items(order, cart_items)
    _clear_cart(request)

    return order    