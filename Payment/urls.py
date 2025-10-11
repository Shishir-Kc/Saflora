from django.urls import path
from .views import payment

app_name = "Payment"

urlpatterns = [
    path('esewa/',payment,name="esewa_payment"),
    path('khalti/',payment,name="Khalti_payment"),    
]
