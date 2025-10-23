from django.urls import path
from .views import in_home,base_navbar

app_name = "home"


urlpatterns = [
    path('',in_home,name="in_home"),
    path('navbar/',base_navbar,name="base_navbar")
]
