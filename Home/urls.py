from django.urls import path
from .views import (in_home,
                    base_navbar,
                    products_list,
                    check_out,
                    user_profile,
                    about_us,
                    contact,
                    how_to_use,)


app_name = "home"


urlpatterns = [
    path('',in_home,name="in_home"),
    path('navbar/',base_navbar,name="base_navbar"),
    path('products/view/',products_list,name="products_list"),
    path('checkout/<str:item_name>/<uuid:id>/payment/',check_out,name="check_out"),
    path('user/profile/view/',user_profile,name="user_profile"),
    path('about-us/', about_us, name='about_us'),
    path('contact/', contact, name='contact'),
    path('how-to-use/', how_to_use, name='how_to_use'),
    
]
