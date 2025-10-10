from django.shortcuts import render,redirect
from django.contrib.auth  import authenticate, login ,logout
from django.contrib import messages
from Accounts.models import Saflora_user
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == "POST":
        user_email = request.POST.get("email")
        user_password = request.POST.get("password")
        if not '@' in user_email:
            messages.error(request,'Enter a Valid Gmail ')
            return redirect("login:user_login")
        try:
         user_id = Saflora_user.objects.get(email=user_email)
        except:
            messages.error(request,"User with this email does not exist ! ")
            return redirect("login:user_login")
        
        user = authenticate(request,username=user_id.username, password =user_password)
        if user is not None:
            login(request,user)
            return redirect("home:in_home")

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
        username = request.POST.get("username")
        user_contact = request.POST.get("contact")
        user_address = request.POST.get("address")
        hear_about_us = request.POST.get("referralOther")
        user_first_name = request.POST.get('firstname')
        user_last_name = request.POST.get('lastname')
        # Server-side Validation
        print("==================================================") 
        print(len(user_contact))
        if len(user_contact)< 10 or len(user_contact)>10:
            messages.error(request,"Contact number must be 10 digits !")
            return render(request, "sign_up/sign_up.html")
        if '@' not in user_email:
            messages.error(request,"Enter a valid email !")
            return render(request, "sign_up/sign_up.html")    

        if Saflora_user.objects.filter(email=user_email,contact=user_contact).exists():
            messages.error(request,"User with that email already exists !")
            return render(request, "sign_up/sign_up.html")
        else:
            user  = Saflora_user.objects.create_user(username=username,email=user_email,password=user_password,contact = user_contact,address=user_address,hear_about_us=hear_about_us,first_name = user_first_name,last_name=user_last_name)

            user.save()
            print("account crated ! ")
            messages.success(request,"Account created please login  ")
            return redirect("login:user_login")
        
    return render(request, "sign_up/sign_up.html")


def user_logout(request):
    logout(request)
    return render(request,"login/login.html")    
