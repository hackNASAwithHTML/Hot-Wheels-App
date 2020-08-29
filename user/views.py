from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from .forms import UserRegisterForm
from django.contrib.auth.models import User
import hashlib
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def signup_function(request):
    if request.method == "POST":
        data = request.POST
        hashed_password = hashlib.sha256(data['password'].encode())
        updated_password = hashed_password.hexdigest()
        user = User.objects.create_user(data['username'],'',updated_password)
        return redirect('log_in')
    return render(request,'user_signup.html')

def login_function(request):
    if request.method == "POST":
        data = request.POST
        hashed_password = hashlib.sha256(data['password'].encode())
        updated_password = hashed_password.hexdigest()
        user = authenticate(username=data['username'],password=updated_password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Username or password is wrong Owo Who are you?')
    return render(request,'user_login.html')

def logout_session(request):
    logout(request)
    return redirect('home')

