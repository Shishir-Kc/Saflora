from django.urls import path
from .views import (user_login
                    ,user_signup,
                    user_logout,
                    forgot_pass,
                    verify_otp,
                    reset_pass,rsend_otp)


app_name = "login"

urlpatterns = [
    path('',user_login,name="user_login"),
    path('user/signup/',user_signup,name='user_signup'),
    path('user/logout/',user_logout,name="user_logout"),
    path('forgot/password/',forgot_pass,name="forgot_pass"),
    path('forgot/password/otp/verify/',verify_otp,name="otp_verify"),
    path('forgot/password/reset/',reset_pass,name="reset_pass"),
    path('forgot/password/otp/resend/',rsend_otp,name="resend_otp"),
]


