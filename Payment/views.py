from django.shortcuts import render,redirect
from django.http import HttpResponse
import json
import requests
from django.urls import reverse
from dotenv import load_dotenv
import os 
from Accounts.models import Saflora_user,Saflora_Product,Cart
from django.contrib import messages
from .models import Payment_Records
import hmac, hashlib, base64
load_dotenv()



khalti_key = os.environ.get('KHALTI_SECRET_KEY')

def payment(request):
    return HttpResponse("This is a payment Page ! ")



def khalti_payment(request,id,cart_id):
  if request.method == "POST":
     print("POST")
     print(request.POST.get('quantity'))
     product = Saflora_Product.objects.get(id=id)
     cart = Cart.objects.create(product=product)
     try:
      user = Saflora_user.objects.get(username=request.user)
     except:
        messages.error(request,"User Does not exists !")
        return redirect("payment:khalti_payment") # need to add proper payment page !

     amount = 10
     amount = (int(amount)*100) # converting rupeese in paisa 
     print(amount)
     url = f'{os.environ.get('KHALTI_BASE_URL')}{os.environ.get("KHALTI_PAYMENT_URL")}'

     payload = json.dumps({
     "return_url": request.build_absolute_uri(reverse('payment:validate_khalti_payment',kwargs={'cart_id':cart_id})),
     "website_url": request.build_absolute_uri('/'),
     "amount": amount,
     "purchase_order_id": str(cart.id),
     "purchase_order_name": product.name,
     "customer_info": {
     "name": f"{user.first_name} {user.last_name}",
     "email": f"{user.email}",
     "phone": f"{user.contact}"
     }
        })
     headers = {
     'Authorization': f'key {khalti_key}',
     'Content-Type': 'application/json',
     }
     try:
         response = requests.request("POST", url, headers=headers, data=payload)
         amount = float(amount)/100 # converting paisa back to rupese 
         payment = Payment_Records.objects.create(user=user,pidx=response.json()['pidx'],total_amount=amount,product=product)
         payment.status = payment.Status.INITIATED
         payment.provider = payment.Payment_Provider.KHALTI
         payment.save() 
         print("PAYMENT SAVED")        
         return_url = (response.json()['payment_url'])
     except KeyError:
         return redirect("home:in_home")

     return redirect (return_url)
  else:
      return render (request,'payment/summary.html') 

def validate_khalti_payment(request,cart_id):
   if request.method  != "POST":  
    print("RECIVED DATA ! ")
    print(Cart.objects.get(id=cart_id))
    pidx =  request.GET.get('pidx')
    url  =f'{os.environ.get("KHALTI_BASE_URL")}{os.environ.get("KHALTI_PAYMENT_VERIFICATION")}'
    payload = json.dumps({
        'pidx':pidx
    })
    headers = {
        'Authorization':f'key {khalti_key}',
        'Content-Type':'application/json'
    }
    try:
        response = requests.request("POST",url=url,data=payload,headers=headers)
    except:
        response = {
            'payment':'error'
        }
    response = response.json()
    try:

       payment_record = Payment_Records.objects.get(pidx=response['pidx'])
       recived_amount = response['total_amount'] 
       recived_pidx = response['pidx']
       if (float(recived_amount)/100) == payment_record.total_amount and recived_pidx == payment_record.pidx: # converting paisa into rupeese for validation  !
           recived_response = response['status']
           cart = Cart.objects.get(id=cart_id)
           if recived_response == "Completed":
            status = Payment_Records.Status.COMPLETED
            cart.cart_status = Cart.Status.PURCHASED
           elif recived_response == "Pending":
              status = Payment_Records.Status.PENDING
           elif recived_response == "Refused":
              status = Payment_Records.Status.FAILED
           elif recived_response == "Expired":
              status = Payment_Records.Status.FAILED
           elif recived_response == "User cancled":
              status = Payment_Records.Status.FAILED
           else:
            status = Payment_Records.Status.FAILED
            messages.error(request,'Invalid Payment Session')
            return redirect("home:in_home")
           
           payment_record.service_provider_status = status
           payment_record.transaction_id = response['transaction_id']
           payment_record.fee = float(response['fee'])/100
           payment_record.status = Payment_Records.Status.COMPLETED
           print(f"Fee:{response['fee']}")
           cart.save()
           payment_record.save()

       else:
            messages.error(request,"Missguided payment !")
            return redirect('home:in_home') 
    except:
       messages.error(request,"Payment Does not exist")
       return render("home:in_home")
    
    print(response)
    return redirect("home:in_home") # it is just for teting purpose !
"""

 what we can do next is runa background process to delete unsucessful transaction ? 


"""
# next we need to integrate esewa !
def esewa_payment(request):
    amount = "100"
    tax_amount = "10"
    total_amount = "110"
    transaction_uuid = "241028"
    product_code = "EPAYTEST"
    secret_key = "8gBm/:&EnhH.1/q("  # UAT secret key
    success_url = "https://developer.esewa.com.np/success"
    failure_url = "https://developer.esewa.com.np/failure"
    signed_field_names = "total_amount,transaction_uuid,product_code"
    data_to_sign = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    signature = base64.b64encode(
        hmac.new(secret_key.encode(), data_to_sign.encode(), hashlib.sha256).digest()
    ).decode()

    context = {
        "amount": amount,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "transaction_uuid": transaction_uuid,
        "product_code": product_code,
        "product_service_charge": "0",
        "product_delivery_charge": "0",
        "success_url": success_url,
        "failure_url": failure_url,
        "signed_field_names": signed_field_names,
        "signature": signature,
        "epay_url": "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
    }
    return render(request, "payment/esewa.html", context)


