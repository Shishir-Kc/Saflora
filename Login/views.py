from django.shortcuts import render,redirect
from django.contrib.auth  import authenticate, login ,logout
from django.contrib import messages
from Accounts.models import Saflora_user
from django.contrib.auth.decorators import login_required
from .tools import does_user_exists
from .models import Verification_code
from Accounts.models import Saflora_user
from celery import shared_task
from .tasks import send_verification_email

def user_login(request):
    if request.method == "POST":
        user_email = request.POST.get("email")
        user_password = request.POST.get("password")
        print("==================================================")
        print(user_email,user_password)
        if not '@' in user_email:
            messages.error(request,'Enter a Valid Gmail ')
            return redirect("login:user_login")
        try:
         user_id = Saflora_user.objects.get(email=user_email)
         print('============================================================')
         print(user_id)
        except:
            messages.error(request,"User with this email does not exist ! ")
            return redirect("login:user_login")
        
        user = authenticate(request,username=user_id.username, password =user_password)
        print(user)
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
        print(user_email)
        if len(user_contact)< 10 or len(user_contact)>10:
            messages.error(request,"Please enter valid contact number ")
            print("contact  is invalid ")
            return render(request, "sign_up/sign_up.html") #ok from server! 
        if '@' not in user_email:
            messages.error(request,"Enter a valid email !")
            print("invalid email ! ")
            return render(request, "sign_up/sign_up.html")    
        if Saflora_user.objects.filter(username=username).exists():
            messages.error(request,"Username already taken !")
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


def forgot_pass(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not does_user_exists(email=email):
            print("user no !")
            messages.error(request,'User does not exists ! ')
            return redirect("login:forgot_pass")
        
        request.session['pending_email'] = email
        try:
         is_send = send_verification_email.delay(email=[email],code=Verification_code.generate_code(email=email).code)
         return redirect("login:otp_verify")
        except Exception as e:
            messages.error(request,"Error Email Could not be sent ! ")
            return render(request,"reset_pass/email.html",)

    return render (request,"reset_pass/email.html")

def rsend_otp(request):
    email = request.session['pending_email']
    try:
         is_send = send_verification_email(email=[email],code=Verification_code.generate_code(email=email).code)
         messages.success(request,"OTP Resent Successfully ! ")
         return redirect("login:otp_verify")
    except Exception as e:
            messages.error(request,"Error Email Could not be sent ! ")
            return redirect("login:otp_verify")

def verify_otp(request):
    if request.method == "POST":
        code = request.POST.get("code")
        email = request.session['pending_email']
        try:
            user = Saflora_user.objects.get(email=email)
        except Saflora_user.DoesNotExist:
            messages.error(request,'User with taht email does not exists ! ')
        except Verification_code.DoesNotExist:
            messages.error(request,'Invalid Code ! ')
        try:
            Validated = Verification_code.objects.get(code=code)
        except Verification_code.DoesNotExist:
            messages.error(request,'Invalid Code ! ')
            return redirect("login:otp_verify")
        
        if Validated:
            Validated.is_used = True
            Validated.save()
            return redirect("login:reset_pass")
    return render(request,"reset_pass/code.html")


def reset_pass(request):
    if request.method == "POST":
        new_pass = request.POST.get("new_pass")
        confirm_pass = request.POST.get("confirm_pass")
        email = request.session['pending_email']
        if new_pass != confirm_pass:
            messages.error(request,"Password do not match ! ")
            return redirect("login:reset_pass")
        try:
            user = Saflora_user.objects.get(email=email)
            user.set_password(new_pass)
            user.save()
            print("============================================")
            print(user.check_password(new_pass))
            messages.success(request,"Password Reset Successful ! Please Login ")
            return redirect("login:user_login")
        except Saflora_user.DoesNotExist:
            messages.error(request,'User with that email does not exists ! ')
            return redirect("login:forgot_pass")

    
    return render(request,"reset_pass/pass.html")


