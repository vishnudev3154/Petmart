from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from . models import *
from django.contrib import messages
from django.contrib.auth.models import User


# admin page 
def adminlogin(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username=='admin' and password=='admin123':
        return redirect(adminpage)
        
    return render(request, 'adminlogin.html')

def adminpage(request):
    return render(request, 'adminpage.html')

def manageproduct(request):
    return render(request, 'manageproduct.html')


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
        
    return render(request, 'addproduct.html')



def viewproduct(request):
    products = petdetails.objects.all()
    return render(request, 'viewproduct.html', {'products': products})




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

    return render(request, 'updateview.html', {'product': product})




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
    return render(request, 'login.html')