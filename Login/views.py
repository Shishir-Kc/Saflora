from django.shortcuts import render
from django.contrib.auth  import authenticate, login ,logout
from django.contrib import messages
from User.models import Saflora_user

def user_login(request):
    if request.method == "POST":
        user_email = request.POST.get("email")
        user_password = request.POST.get("password")
        user = authenticate(request,username =user_email, password =user_password)
        if user is not None:
            login(request,user)

        else:    
         print("Invalid Credentials")
         messages.error(request,"Invalid Credentials ! ")
         return render(request, "login/login.html")
    else:
        return render(request, "login/login.html")
    
def user_signup(request):
    if request.method == "POST":
        user_email = request.POST.get("email")
        user_password = request.POST.get("password")
        username = request.POSt.get("username")
        user_contact = request.POST.get("contact")
        if Saflora_user.objects.filter(email=user_email,contact=user_contact).exists():
            messages.error(request,"User with that email already exists !")
            return render(request, "login/signup.html")
        else:
            user  = Saflora_user.objects.create_user(username=username,email=user_email,password=user_password,contact = user_contact)
            user.save()
            messages.success(request,"User Account Created Successfully !")
            return render(request, "login/login.html")
    return render(request, "login/signup.html")


def user_logout(request):
    logout(request)
    return render(request,"login/login.html")    
