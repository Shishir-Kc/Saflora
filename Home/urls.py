from django.urls import path
from .views import in_home,base_navbar,products_list,check_out

app_name = "home"


urlpatterns = [
    path('',in_home,name="in_home"),
    path('navbar/',base_navbar,name="base_navbar"),
    path('products/view/',products_list,name="products_list"),
    path('checkout/<str:item_name>/<uuid:id>/payment/',check_out,name="check_out"),
]
