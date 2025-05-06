from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (PostListView,PostCreateView,PostDetailView,PostUpdateView,PostDeleteView,CategoryListView,SearchResultsView, PrivacyPolicyView)

app_name = 'techmarket'
#URL patterns
urlpatterns = [
    path('', views.home, name='home'), 
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('category/<slug:category_slug>/', PostListView.as_view(), name='product-list-by-category'),
    path('products/', PostListView.as_view(), name='product-list'),
    path('products/new/', PostCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/', PostDetailView.as_view(), name='product-detail'),
    path('search/', SearchResultsView.as_view(), name='search_products'),
    path('product/<int:pk>/edit/', PostUpdateView.as_view(), name='product-edit'),
    path('product/<int:pk>/delete/', PostDeleteView.as_view(), name='product-delete'),
    path('add-to-basket/<int:product_id>/', views.add_to_basket, name='add-basket'),
    path('basket/', views.view_basket, name='basket-view'),
    path('basket/remove/<int:product_id>/', views.basket_remove, name='basket-remove'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('confirm-payment/', views.confirm_payment_view, name='confirm-payment'),
    path('process-payment/', views.process_payment, name='process-payment'),
    path('order-confirmation/', views.order_confirmation_view, name='order-confirmation'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)