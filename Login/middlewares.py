from django.shortcuts import redirect


class is_Loggedin:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
         restricted_path = [
              '/accounts/login/',
              '/accounts/login/user/signup/',
              '/accounts/login/forgot/password/',
              '/accounts/login/forgot/password/otp/verify/',
              '/accounts/forgot/password/reset/',
              '/accounts/forgot/password/otp/resend/',
              '/landing_page/Saflora'
              

         ]
         
         if request.user.is_authenticated and request.path in restricted_path:

            return redirect('home:home')   
         
         return self.get_response(request)