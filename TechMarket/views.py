from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm, Contact
import decimal
from django.contrib.auth.decorators import login_required

#Home Page
def home(request):
    return render(request, 'techmarket/home.html', {'title': 'Home'})
#About page
def about(request):
    return render(request, 'techmarket/about.html', {'title': 'About'})
#Contact submisson and sends email
def contact(request):
    if request.method == "POST":
        form = Contact(request.POST)
        if form.is_valid():
            Firstname = form.cleaned_data["Firstname"]
            Surename = form.cleaned_data["Surename"]
            Email = form.cleaned_data["Email"]
            Address = form.cleaned_data["Address"]
            Phonenumber = form.cleaned_data["Phonenumber"]
            Message = form.cleaned_data["Message"]
            email_message = EmailMessage(
                subject=f"Contact Form from {Firstname,Surename}",
                body=Message,
                from_email= Email,
                to=["noreply@SHU.com"],
                reply_to=[Email],
            )
            email_message.send()
            messages.success(request, "Your message has been received!")
            form = Contact() 

        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = Contact()

    return render(request, 'techmarket/contact.html', {'form': form, 'title': 'Contact'})
#Search view
class SearchResultsView(ListView):
    model = Product
    template_name = 'techmarket/search_products.html'
    context_object_name = 'products'
    ordering = ['-date_posted']
    paginate_by = 5
#Prdcut list
class PostListView(ListView):
    model = Product
    template_name = 'techmarket/products.html'
    context_object_name = 'products'
    ordering = ['-date_posted']
    # catagory 
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        query = self.request.GET.get('q')

        print(f"--- Search Query Received: '{query}' ---")

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            ).distinct()

        print(f"--- Queryset Count After Filtering: {queryset.count()} ---")
        return queryset.order_by('-date_posted')
    #Page tiles
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        query = self.request.GET.get('q', '')
        context['search_query'] = query

        if category_slug:
            context['category'] = get_object_or_404(Category, slug=category_slug)
            if query:
                context['title'] = f'Search "{query}" in {context["category"].name}'
            else:
                context['title'] = f'Category: {context["category"].name}'
        else:
            if query:
                context['title'] = f'Search results for "{query}"'
            else:
                context['title'] = 'All Products'
        return context
#Product detail
class PostDetailView(DetailView):
    model = Product
    template_name = 'techmarket/product_detail.html'
#Product create
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'techmarket/product_form.html'
    fields = ['name', 'description', 'price', 'category', 'image']

    def form_valid(self, form):
        form.instance.seller = self.request.user
        messages.success(self.request, 'Product listed successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('techmarket:product-list')
#Product update
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'techmarket/product_form.html'
    fields = ['name', 'description', 'price', 'category', 'image']

    def form_valid(self, form):
        messages.success(self.request, 'Product updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.seller

    def get_success_url(self):
        return reverse('techmarket:product-detail', kwargs={'pk': self.object.pk})
#Product Delete
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'techmarket/product_confirm_delete.html'

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.seller

    def form_valid(self, form):
        messages.success(self.request, f'Product "{self.object.name}" deleted successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('techmarket:product-list')

#Category List View
class CategoryListView(ListView):
    model = Category
    template_name = 'techmarket/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product Categories'
        return context

# Basket Views
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    basket = request.session.get('basket', {})
    #Get quantity from POST data, default to 1 if not given
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        basket[str(product_id)] = basket.get(str(product_id), 0) + quantity
        messages.success(request, f'Added {quantity} x "{product.name}" to your basket.')
    else:
        messages.warning(request, 'There is nothing in your basket!.')
    request.session['basket'] = basket
    request.session.modified = True
    return redirect('techmarket:product-list')

def view_basket(request):
    basket = request.session.get('basket', {})
    basket_items = []
    total_price = decimal.Decimal('0.00')
    product_ids = basket.keys()
    products = Product.objects.filter(pk__in=product_ids)

    for product in products:
        product_id_str = str(product.pk)
        quantity = basket[product_id_str]
        item_total = product.price * quantity
        basket_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })
        total_price += item_total
    context = {
        'basket_items': basket_items,
        'total_price': total_price,
        'title': 'Shopping Basket'
    }
    return render(request, 'techmarket/basket.html', context)

def basket_remove(request, product_id):
    basket = request.session.get('basket', {})
    product_id_str = str(product_id) # Session keys must be strings

    if product_id_str in basket:
        del basket[product_id_str]
        request.session['basket'] = basket
        request.session.modified = True # Mark session as modified
        messages.success(request, 'Item has been removed from your basket.') #message
    else:
        messages.warning(request, 'No item found in your basket.')

    return redirect('techmarket:basket-view')
#chechout for payment
@login_required
def checkout_view(request):
    basket = request.session.get('basket', {})
    basket_items = []
    total_price = decimal.Decimal('0.00')
    product_ids = basket.keys()
    products = Product.objects.filter(pk__in=product_ids)
    product_map = {str(p.pk): p for p in products}
    for product_id_str, quantity in basket.items():
        product = product_map.get(product_id_str)
        if product and product.price is not None:
            item_total = product.price * quantity
            basket_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })
            total_price += item_total

    context = {
        'basket_items': basket_items,
        'total_price': total_price,
        'title': 'Checkout Summary'
    }
    return render(request, 'techmarket/checkout.html', context)
#confirm order
@login_required
def confirm_payment_view(request):
    # Re-fetch basket details to display on confirmation page
    basket = request.session.get('basket', {})
    if not basket:
        messages.warning(request, "Your basket is empty.")
        return redirect('techmarket:basket-view')
        
    basket_items = []
    total_price = decimal.Decimal('0.00')
    product_ids = basket.keys()
    products = Product.objects.filter(pk__in=product_ids)
    product_map = {str(p.pk): p for p in products}
    for product_id_str, quantity in basket.items():
        product = product_map.get(product_id_str)
        if product and product.price is not None:
            item_total = product.price * quantity
            basket_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })
            total_price += item_total
        else:
            messages.error(request, f"Could not find product ID {product_id_str} in basket for confirmation.")
            return redirect('techmarket:basket-view')
            
    context = {
        'basket_items': basket_items,
        'total_price': total_price,
        'title': 'Confirm Payment'
    }
    return render(request, 'techmarket/confirm_payment.html', context)
#Simulates deleted product after "payment"
@login_required
def process_payment(request):
    if request.method == 'POST':
        basket = request.session.get('basket', {})
        product_ids_to_delete = list(basket.keys()) #Gets product IDs before clearing

        if product_ids_to_delete:
            try:
                #Convert IDs to integers for the query
                product_ids_int = [int(pid) for pid in product_ids_to_delete]
                products_to_delete = Product.objects.filter(pk__in=product_ids_int)
                count, _ = products_to_delete.delete()
                print(f"Deleted {count} Product objects from database.") # Debugg

            except ValueError:
                messages.error(request, "Error processing product IDs in basket.")
                return redirect('techmarket:basket-view')
            except Exception as e:
                 messages.error(request, f"An error occurred while deleting products: {str(e)}")
                 return redirect('techmarket:basket-view')
        
        #Clear the basket
        if 'basket' in request.session:
            del request.session['basket']
            request.session.modified = True
            print("Basket cleared after payment.") # Debug
        else:
            print("No basket found in session to clear.") # Debug
        
        messages.success(request, "Your payment was successful, the items were removed from your basket, and the product listings were deleted.")
        #redirect to the home page
        return redirect('techmarket:home') 
    else:
        #redirect if accessed via GET
        messages.error(request, "Invalid request method.")
        return redirect('techmarket:basket-view')
# Oder Confirm
def order_confirmation_view(request):
    return render(request, 'techmarket/order-confirmation.html', {'title': 'Order Confirmed'})
# prolicy page
class PrivacyPolicyView(TemplateView):
    template_name = 'techmarket/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Privacy Policy'
        return context
