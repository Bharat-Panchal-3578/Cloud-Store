from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

User = get_user_model()

# Create your views here.
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user, backend='users.backends.EmailBackend')

        return redirect('home')
    return render(request, 'users/signup.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email , password=password)

        if user is not None:
            login(request, user, backend='users.backends.EmailBackend')
            return redirect('home')
        
        messages.error(request, "Invalid email or password.")
        return redirect('login')
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')