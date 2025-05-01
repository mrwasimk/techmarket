from django.urls import path
from . import views


app_name = 'techmarket'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('categories/', views.category_list, name='category-list'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),
    path('basket/', views.basket_view, name='basket-view'),
    path('basket/add/<int:product_id>/', views.basket_add, name='basket-add'),
    path('basket/remove/<int:product_id>/', views.basket_remove, name='basket-remove'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-confirmation/', views.order_confirmation_view, name='order-confirmation'), 
]
