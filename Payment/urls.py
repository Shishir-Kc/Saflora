from django.urls import path
from .views import payment,khalti_payment,validate_khalti_payment,esewa_payment

app_name = "payment"

urlpatterns = [
    path('esewa/',esewa_payment,name="esewa_payment"),
    path('khalti/',khalti_payment,name="Khalti_payment"),   
    path('khalti/verification/',validate_khalti_payment,name='validate_khalti_payment'), 
]
