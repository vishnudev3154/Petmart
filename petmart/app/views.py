from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User



# admin page 
def adminlogin(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username=='admin' and password=='admin123':
        return redirect(adminpage)
        
    return render(request, 'admin/adminlogin.html')

def adminpage(request):
    return render(request, 'admin/adminpage.html')

def manageproduct(request):
    return render(request, 'admin/manageproduct.html')


def addproduct(request):
    if request.method=='POST':
        name=request.POST['name']
        category=request.POST['category']
        description=request.POST['description']
        pet_price=request.POST['pet_price']
        pet_image = request.FILES.get('pet_image')
        data=petdetails.objects.create(name=name,category=category,description=description,pet_price=pet_price,pet_image=pet_image)
        print (data)
        data.save()
        
    return render(request, 'admin/addproduct.html')



def viewproduct(request):
    products = petdetails.objects.all()
    return render(request, 'admin/viewproduct.html', {'products': products})




def viewproductupdate(request, pk):
    product = get_object_or_404(petdetails, pk=pk)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.category = request.POST['category']
        product.description = request.POST['description']
        product.pet_price = request.POST['pet_price']

        if request.FILES.get('pet_image'):
            product.pet_image = request.FILES['pet_image']

        product.save()
        return redirect(viewproduct)

    return render(request, 'admin/updateview.html', {'product': product})




def viewproductdelet(request,pk):
    product=get_object_or_404(petdetails,pk=pk)
    product.delete()
    return redirect(viewproduct)


# user page  
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        # 1️⃣ Check passwords match
        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        # 2️⃣ Check username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect(register)

        # 3️⃣ Check email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        # 4️⃣ Create user (password is hashed automatically)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "user/register.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful")
            return redirect('viewproduct')   # or any dashboard page
        else:
            messages.error(request, "Invalid username or password")
            return redirect(login)

    return render(request, 'user/login.html')


def userpage(request):
    product = petdetails.objects.all()
    return render(request, 'user/userpage.html',{'products':product})

from django.contrib.auth.decorators import login_required
from .models import Cart, Wishlist, petdetails


def add_to_cart(request, pk):
    product = get_object_or_404(petdetails, pk=pk)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, "Added to cart")
    return redirect('viewproduct')



def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.pet_price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })



def remove_from_cart(request, pk):
    Cart.objects.filter(id=pk, user=request.user).delete()
    return redirect('viewcart')



def add_to_wishlist(request, pk):
    product = get_object_or_404(petdetails, pk=pk)
    Wishlist.objects.get_or_create(
        user=request.User,
        product=product
    )
    messages.success(request, "Added to wishlist")
    return render(request,'userpage.html')



def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.User)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})



def remove_from_wishlist(request, pk):
    Wishlist.objects.filter(id=pk, user=request.user).delete()
    return redirect('wishlist')
