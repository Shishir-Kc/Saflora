from django.urls import path
from .views import (in_home,
                    base_navbar,
                    products_list,
                    check_out,
                    user_profile,
                    about_us,
                    contact,
                    how_to_use,
                    cart,
                    add_to_cart,
                    update_address,
                    update_profile,
                    delete_cart,
                    index_home

                    )


app_name = "home"


urlpatterns = [
    path('home/',index_home,name="home"),
    path('',in_home,name="in_home"),
    path('navbar/',base_navbar,name="base_navbar"),
    path('products/view/',products_list,name="products_list"),
    path('checkout/<uuid:id>/payment/',check_out,name="check_out"),
    path('checkout/<uuid:id>/payment/<uuid:cart_id>/',check_out,name="check_out_cart"),
    path('user/profile/view/',user_profile,name="user_profile"),
    path('about-us/', about_us, name='about_us'),
    path('contact/', contact, name='contact'),
    path('how-to-use/', how_to_use, name='how_to_use'),
    path('user/cart/',cart,name="cart"),
    path('user/cart/add/<uuid:product_id>/',add_to_cart,name="add_to_cart"),
    path('user/update/account/',update_profile,name="update_profile"),
    path('user/update/address/',update_address,name="update_address"),
    path('user/delete/cart/<uuid:id>/',delete_cart,name="delete_cart")
    
]
