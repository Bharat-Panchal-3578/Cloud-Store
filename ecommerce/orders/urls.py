from django.urls import path
from orders.views import checkout_view, order_confirmation_view, order_list_view, order_detail_view

urlpatterns = [
    path('', order_list_view, name='order_list'),
    path('<int:order_id>/', order_detail_view, name='order_detail'),
    path('checkout/', checkout_view, name='checkout'),
    path('confirmation/<int:order_id>/', order_confirmation_view, name='order_confirmation'),
]