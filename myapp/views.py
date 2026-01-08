from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Feature
from django.contrib.auth.models import User, auth
from django.contrib import messages

def index(request):
    features = Feature.objects.all()
    return render(request, 'index.html',{'features': features})

def download(request):
    return HttpResponse("<h1> You are here to download something....</h1>")

def counter(request):
    words = request.GET['words']
    count = len(words.split())
    return render(request,'counter.html', {'count':count})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:

            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('register')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('register')

            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                messages.success(request, 'Account created successfully')
                return redirect('login')

        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')

    return render(request, 'register.html')
def login(request):
    # If form is submitted
    if request.method == 'POST':
        # Get data from form
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = auth.authenticate(username=username, password=password)

        # If user exists
        if user is not None:
            auth.login(request, user)   # Login user
            return redirect('/')        # Redirect to home page
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')

    # If request method is GET
    return render(request, 'login.html')

              
    
