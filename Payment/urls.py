from django.urls import path
from .views import khalti_payment,validate_khalti_payment

app_name = "payment"

urlpatterns = [
    # path('esewa/',esewa_payment,name="esewa_payment"),
    path('khalti/<uuid:id>/cart/<uuid:cart_id>/',khalti_payment,name="Khalti_payment"),   
    path('khalti/verification/<uuid:cart_id>/',validate_khalti_payment,name='validate_khalti_payment'), 
]
