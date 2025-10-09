from django.urls import path
from .views import user_login


app_name = "login"

urlpatterns = [
    path('',user_login,name="user_login")
]


