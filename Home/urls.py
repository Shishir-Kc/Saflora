from django.urls import path
from .views import in_home

app_name = "home"


urlpatterns = [
    path('',in_home,name="in_home")
]
