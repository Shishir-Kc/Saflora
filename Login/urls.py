from django.urls import path
from .views import user_login,user_signup


app_name = "login"

urlpatterns = [
    path('',user_login,name="user_login"),
    path('user/signup/',user_signup,name='user_signup'),
]


