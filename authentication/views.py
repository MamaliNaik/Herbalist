from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            # messages.warning(request, "Passwords do not match")
            return render(request, 'authentication/signup.html')

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")

        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered")

        user = User.objects.create_user( username=username, email=email, password=password1 )
        user.save()

        return redirect('/auth/login/')

    return render(request, 'authentication/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'authentication/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'authentication/login.html')
# def login(request):
#     return render(request, 'authentication/login.html')


def logout(request):
    auth_logout(request)
    return redirect('/auth/login/')
