from django.shortcuts import render
from django.contrib.auth  import authenticate, login 

def user_login(request):
    if request.method == "POST":
        user_email = request.POST.get("email")
        user_password = request.POST.get("password")
        user = authenticate(request,username =user_email, password =user_password)
        if user is not None:
            login(request,user)
        
    else:
        return render(request, "login/login.html")