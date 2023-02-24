from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib import messages
# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect("acc:login")

    return render(request,'acc/index.html')

def ulogin(request):
    
    if request.user.is_authenticated:
        return redirect("acc:index")

    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        u = authenticate(username=un, password=up)
        if u:
            login(request, u)
            messages.success(request, f"{u} 님 환영합니다!")
            return redirect("acc:index")
        else:
            messages.info(request, "계정 정보가 일치하지 않습니다")
    return render(request, "acc/login.html")

def ulogout(request):
    logout(request)
    return redirect("acc:login")

def signup(request):

    if request.user.is_anonymous:
        return redirect("board:index")

    if request.method == "POST":
        un = request.POST.get('uname')
        up = request.POST.get("upass")
        rk = request.POST.get("urank")
        try:
            User.objects.create_user(username=un, password=up,rank = rk)
            return redirect("acc:login")
        except:
            pass 
    return render(request, "acc/signup.html")