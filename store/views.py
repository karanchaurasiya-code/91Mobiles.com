from django.shortcuts import render, redirect
from .models import Product , Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm
from django import forms

def category(request, foo):
    foo = foo.replace('-', '')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {
            'products': products,  # <-- fix this line
            'category': category
        })
    except:
        messages.success(request, "That Category Doesn't Exist......")
        return redirect('home')


# Create your views here.
def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})


def home(req):
    products = Product.objects.all()
    return render(req, 'home.html', {'products': products})


def about(req):
    return render(req, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been Logged in !!"))
            return redirect("home")
        else:
            messages.success(request, ("something is worng please try agein "))
            return redirect("login")
    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(
        request, ("You have been logged out... Thanks for stopping by ....."))
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have Registered Successfully! Welcome")
                return redirect('home')
            else:
                messages.error(request, "Authentication failed after registration.")
                return redirect('login')  # fallback if authentication fails
        else:
            messages.error(request, "Something is wrong. Please check the form again.")
            return render(request, 'register.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import UpdateUserForm

@login_required
def update_user(request):
    current_user = request.user
    user_form = UpdateUserForm(request.POST or None, instance=current_user)
    
    if request.method == "POST":
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)  # Re-authenticate if needed
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('home')
        else:
            messages.error(request, "There was an error updating your profile.")

    return render(request, 'update_user.html', {'user_form': user_form})

