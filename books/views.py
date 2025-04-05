from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User  # Ensure User model is imported
from django.http import HttpResponse
from .models import Book
from django.contrib import messages
from .models import Order   
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
def home(request):
    return render(request, 'books/home.html')    

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

@login_required(login_url='login')
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.book.price for item in cart_items)
    return render(request, 'books/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def order_view(request):
    return render(request, 'books/order.html')  # Ensure 'order.html' exists

@login_required(login_url='login')  # Redirects to login page if not logged in
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.user.is_authenticated:
        CartItem.objects.create(book=book, user=request.user)
    else:
        return redirect('login')  # Redirect if user is not logged in

    return redirect('cart')

@login_required(login_url='login')
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if cart_items.exists():
        order = Order.objects.create(user=request.user)
        for item in cart_items:
            order.books.add(item.book)
        order.save()

        cart_items.delete()
        messages.success(request, "✅ Checkout complete! Your order has been placed.")
    else:
        messages.info(request, "🛒 Your cart was already empty.")
        
    return redirect('cart')
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "🎉 Account created! You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'books/register.html', {'form': form})

@login_required(login_url='login')
def remove_from_cart(request, book_id):
    cart_item = CartItem.objects.filter(book_id=book_id, user=request.user).first()
    if cart_item:
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not found in your cart.")
    return redirect('cart')

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout

class CustomLoginView(LoginView):
    template_name = 'books/login.html'
