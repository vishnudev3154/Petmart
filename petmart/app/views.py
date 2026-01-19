from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from datetime import date, timedelta


#    ADMIN SECTION 


def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "admin" and password == "admin123":
            request.session["is_admin"] = True
            return redirect("adminpage")

        messages.error(request, "Invalid admin credentials")

    return render(request, "admin/adminlogin.html")


def adminpage(request):
    return render(request, "admin/adminpage.html")


def addproduct(request):
    if request.method == "POST":
        petdetails.objects.create(
            category=request.POST.get("category"),
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            pet_price=request.POST.get("pet_price"),
            stock=request.POST.get("stock", 0),
            pet_image=request.FILES.get("pet_image"),
        )
        messages.success(request, "Product added successfully")
        return redirect("manageproduct")

    return render(request, "admin/addproduct.html")


def manageproduct(request):
    products = petdetails.objects.all()
    return render(request, "admin/manageproduct.html", {"products": products})


def viewproductupdate(request, pk):
    product = get_object_or_404(petdetails, pk=pk)

    if request.method == "POST":
        product.category = request.POST.get("category")
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.pet_price = request.POST.get("pet_price")
        product.stock = request.POST.get("stock")

        if request.FILES.get("pet_image"):
            product.pet_image = request.FILES.get("pet_image")

        product.save()
        messages.success(request, "Product updated successfully")
        return redirect("manageproduct")

    return render(request, "admin/updateview.html", {"product": product})


def viewproductdelet(request, pk):
    product = get_object_or_404(petdetails, pk=pk)
    product.delete()
    messages.success(request, "Product deleted")
    return redirect("manageproduct")


def is_admin(user):
    return user.is_superuser


def view_users(request):
    users = User.objects.all()
    return render(request, "admin/viewuser.html", {"users": users})

def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, "admin/view_orders.html", {"orders": orders})


def admin_logout(request):
    request.session.pop('is_admin', None)
    messages.success(request, "Admin logged out successfully")
    return redirect('adminlogin')


# ===================== USER AUTH =====================

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created. Please login.")
        return redirect("login")

    return render(request, "user/register.html")


def login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user:
            auth_login(request, user)
            messages.success(request, "Login successful")
            return redirect("userpage")

        messages.error(request, "Invalid credentials")

    return render(request, "user/login.html")


@login_required(login_url="login")
def userpage(request):
    category = request.GET.get("category")
    search = request.GET.get("search")

    products = petdetails.objects.all()

    if category and category != "all":
        products = products.filter(category=category)

    if search:
        products = products.filter(name__icontains=search)

    return render(request, "user/userpage.html", {
        "products": products,
        "selected_category": category,
        "search": search
    })


@login_required(login_url='login')
def profile(request):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()

        messages.success(request, "Profile updated successfully")
        return redirect('profile')

    return render(request, "user/profile.html", {
        "user": user
    })



def logout_view(request):
    logout(request)
    return redirect('login')

# ===================== CART =====================

@login_required(login_url="login")
def add_to_cart(request, pk):
    product = get_object_or_404(petdetails, pk=pk)

    if product.stock <= 0:
        messages.error(request, "Out of stock")
        return redirect("userpage")

    cart_item, created = Cart.objects.get_or_create(
        user=request.user, product=product
    )

    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, "Stock limit reached")
            return redirect("userpage")

    messages.success(request, "Added to cart")
    return redirect("userpage")


@login_required(login_url="login")
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total_price = 0
    cart_data = []

    for item in cart_items:
        subtotal = item.product.pet_price * item.quantity
        total_price += subtotal

        cart_data.append({
            "id": item.id,
            "product": item.product,
            "quantity": item.quantity,
            "subtotal": subtotal,
        })

    return render(
        request,
        "user/cart.html",
        {
            "cart_items": cart_data,
            "total_price": total_price,
        },
    )



@login_required(login_url="login")
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart")
    return redirect("viewcart")


# ===================== WISHLIST =====================

@login_required(login_url="login")
def add_to_wishlist(request, pk):
    product = get_object_or_404(petdetails, pk=pk)

    if Wishlist.objects.filter(user=request.user, product=product).exists():
        messages.info(request, "Already in wishlist")
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, "Added to wishlist")

    return redirect("userpage")


@login_required(login_url="login")
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(
        request, "user/wishlist.html", {"wishlist_items": wishlist_items}
    )


@login_required(login_url="login")
def remove_from_wishlist(request, pk):
    item = get_object_or_404(Wishlist, pk=pk, user=request.user)
    item.delete()
    messages.success(request, "Removed from wishlist")
    return redirect("wishlist")


# ===================== BUY NOW =====================

from django.core.mail import send_mail
from django.conf import settings
from datetime import date, timedelta
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def buy_all_payment(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty")
        return redirect('viewcart')

    total_price = sum(item.subtotal for item in cart_items)

    order_date = date.today()
    delivery_date = order_date + timedelta(days=5)

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            total_amount=total_price,
            status="Completed"
        )

        product_list = []

        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(
                    request,
                    f"Not enough stock for {item.product.name}"
                )
                return redirect('viewcart')

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.pet_price,
                order_date=order_date,
                delivary_date=delivery_date
            )

            product_list.append(
                f"{item.product.name} × {item.quantity} = ₹{item.subtotal}"
            )

            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()

        subject = "🧾 Order Confirmation - PetMart"
        message = f"""
Hello {request.user.username},

Thank you for your purchase! 🎉

Order ID: {order.id}
Order Date: {order_date}
Delivery Date: {delivery_date}

Items:
{chr(10).join(product_list)}

Total Amount: ₹{total_price}

Payment Method: Cash on Delivery

Thank you for shopping with PetMart 🐾
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )

        messages.success(
            request,
            "🎉 Order placed successfully! Confirmation email sent."
        )
        return redirect('userpage')

    return render(request, "user/payment.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "today": order_date,
        "fdate": delivery_date,
    })
