from django.shortcuts import render, redirect # type: ignore
from .models import Product, CartItem, Order
from .forms import ProductForm, RegistrationForm, OrderForm
from django.contrib.auth import login, authenticate# type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def home(request):
    products = Product.objects.all()
    p = Paginator(products, 2)
    page_number = request.GET.get('p')

    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}


    try:
        number_of_items = len(CartItem.objects.filter(user=request.user))
    except:
        number_of_items = 0


    context = {"products": products, "number_of_items": number_of_items, 'page_obj': page_obj}
    return render(request, "home/home.html", context)

def about(request):
    return render(request, "home/about.html")


def details(request, id):
    product = Product.objects.get(id=id)

    context = {"product": product}
    return render(request, "home/details.html", context)

# Create your views here.

@login_required(login_url='user/login')
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")

        
    form = ProductForm()
    context = {"form": form}
    return render(request, "home/add_product.html", context)

def register(request):
    if request.method == "POST":
        user = RegistrationForm(request.POST)
        if user.is_valid():
            user.save()
        
        username = request.POST['username']
        password = request.POST['password1']
        u = authenticate(request,username=username, password=password)

        if u is not None:
            form = login(request, u)
            return redirect('home')

        
    form = RegistrationForm()
    context = {"form": form}
    return render(request, "home/register.html", context)

@login_required(login_url='login')
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart_item, create = CartItem.objects.get_or_create(product=product,user=request.user)
    cart_item.quantity += 1
    cart_item.price = product.price * cart_item.quantity
    cart_item.save()
    return redirect("/")

@login_required(login_url='login')
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = 0
    for i in cart_items:
        total += i.price
    numer_of_items = len(CartItem.objects.filter(user=request.user))
    context = {"cart_items": cart_items, "total_price": total, "number_of_items": numer_of_items}
    print("Total", total)
    return render(request, "home/cart.html", context)

def remove_item(request, id):
    cart_items = CartItem.objects.filter(id=id, user=request.user)
    cart_items.delete()
    return redirect('view_cart')

def checkout(request):
    if request.method == "POST":
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            order = Order()
            order.name = request.POST.get("name")
            order.address = request.POST.get("address")
            order.phone = request.POST.get("phone") 
            order.user = request.user
            order.quantity = item.quantity
            order.price = item.price
            order.product = item.product.name
            order.save()

        for item in cart_items:
            item.delete()

        return redirect("home")

    cart_items = CartItem.objects.filter(user=request.user)
    form = OrderForm()

    total = 0
    for i in cart_items:
        total += i.price
        
    context = {"product": cart_items, "form": form}
    return render(request, "home/checkout.html", context)