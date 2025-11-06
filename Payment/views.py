from django.shortcuts import render,redirect
from django.http import HttpResponse
import json
import requests
from django.urls import reverse
from dotenv import load_dotenv
import os 
from Accounts.models import Saflora_user,Saflora_Product,Cart,AnonymousUser
from django.contrib import messages
from .models import Payment_Records
from .tools import send_notification_saflora,send_notification_user
load_dotenv()



khalti_key = os.environ.get('KHALTI_SECRET_KEY')

def payment(request):
    return HttpResponse("This is a payment Page ! ")



def khalti_payment(request,id,cart_id):
  if request.method == "POST":
     cart = Cart.objects.get(id=cart_id)
     anonymous_user = None

     if request.user.is_authenticated: 
      user = Saflora_user.objects.get(username=request.user)
      full_name = user.get_full_name()
      email = user.email
      address= user.address
      contact_number = user.contact

     if not request.user.is_authenticated:
       try: # - > added a try statement to get full user_info and find the user or create a user if not exists
        full_name = request.POST.get('full_name')
        contact_number = request.POST.get('contact')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get("city")
        province = request.POST.get('province')
        postal_code = request.POST.get('postal_code')

       except: # - > this will run if there is incomplete imformation !
        logging.warning('incomplete user information !')
        messages.error(request,'please provide full information !')
        return redirect("payment:Khalti_payment")
       
       try: # - > try to get Anonymous user with their id , check if the user`s email is in our datbase or not 
           anonymous_user = AnonymousUser.objects.get(email=email)
           """
            user - > Anonymous user 

            What if the user with same same email uses different address ? 
            we havent made a case to store new user address every time they change it ?  
            
            we can simply update the user fields !

            we dont need to update email it will be their unique identification 
            """
           anonymous_user.full_name = full_name
           anonymous_user.contact_number = contact_number
           anonymous_user.shipping_address = address
           anonymous_user.city = city
           anonymous_user.province = province
           anonymous_user.postal_code = postal_code

           anonymous_user.save()
           

       except AnonymousUser.DoesNotExist: # - > if user is not in our database we create one and assign the values 
           anonymous_user = AnonymousUser.objects.create(full_name=full_name,contact_number=contact_number,email=email,shipping_address=address,province=province,city=city,postal_code=postal_code)
       except Exception as e: # - > failsafe will run when it fails to create a user 
         messages.error(request,'Something went wrong!')
         logging.warning("error finding or creating user !")
         return redirect("home:products_list")
   
        
       
        
       

       try:
        
        cart.anonymous_user = anonymous_user
        cart.anonymous_user = AnonymousUser.objects.get(email=anonymous_user.email)
        cart.save()
       except Cart.DoesNotExist:
         messages.error(request,'Your cart does not exists !')
         return redirect("home_products_list")
       except:
            messages.error(request,'something went wrong !')
            return redirect("home:in_home")
       
     
     
     product = Saflora_Product.objects.get(id=id)
     amount = cart.total_price

     

     if anonymous_user:
      payment = Payment_Records.objects.create(anonymous_user=anonymous_user,product=product,total_amount=amount,cart=cart)
     else:
        payment = Payment_Records.objects.create(user=user,product=product,total_amount=amount,cart=cart)
     
     if not cart.payment_method==Cart.Payment_Method.ONLINE:
        payment.payment_method = Payment_Records.Payment_Method.COD
        
        payment.save()
        messages.success(request,'Your order has been placed !')
        send_notification_saflora(cart_id=cart_id)
        send_notification_user(cart_id=cart_id)
        return redirect('home:products_list')
     
     amount = (int(amount)*100) # converting rupeese in paisa 
     url = f'{os.environ.get('KHALTI_BASE_URL')}{os.environ.get("KHALTI_PAYMENT_URL")}'
     return_url = request.build_absolute_uri(reverse('payment:validate_khalti_payment',kwargs={'cart_id':cart_id}))
     payload = json.dumps({
     "return_url": return_url,
     "website_url": request.build_absolute_uri('/'),
     "amount": amount,
     "purchase_order_id": str(payment.id),
     "purchase_order_name": product.name,
     "customer_info": {
     "name": full_name,
     "email": email,
     "phone": contact_number
     }
        })
     headers = {
     'Authorization': f'key {khalti_key}',
     'Content-Type': 'application/json',
     }
     try:
         response = requests.request("POST", url, headers=headers, data=payload)

         payment.pidx=response.json()['pidx']
         payment.status = payment.Status.INITIATED
         payment.provider = payment.Payment_Provider.KHALTI
         payment.payment_method = Payment_Records.Payment_Method.ONLINE
         payment.save()      
         return_url = (response.json()['payment_url'])
     except KeyError:
         messages.error(request,'Some thing went wrong ! ')
         return redirect("home:products_list")

     return redirect (return_url)
  else:
      amount = 0
      product = Saflora_Product.objects.get(id=id)
      cart = Cart.objects.get(id=cart_id)
      if cart.product.discount_price:
         sub_total = int(cart.product.discount_price)*int(cart.quantity)
      else:
        sub_total = int(cart.product.price)*int(cart.quantity)    

      try:
         user = Saflora_user.objects.get(id=request.user.id)
      except:
        user = "None"  
      
      variant= cart.product.variant.all()
      for i in variant:
         variant = i
      if request.user.is_authenticated:
       if not user.location.name == "itahari-4" or user.location.name =="ithari-5":
         amount = 30
      else:
         amount = 30
      cart.total_price = sub_total + amount
      cart.save()
      
      context = { 
         'cart':cart,
         'user':user,
         'sub_total':sub_total,
         'variant':variant,
         'Total':sub_total + amount
      }
      return render (request,'payment/summary.html',context) 

def validate_khalti_payment(request,cart_id):
   if request.method  != "POST":  

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
            payment_record.transaction_id = response['transaction_id']
            cart.cart_status = Cart.Status.PURCHASED
            cart.paid_price = (float(recived_amount)/100) + float(response['fee'])/100
            messages.success(request,"Order has been placed !")
            cart.save()
           elif recived_response == "Pending":
              status = Payment_Records.Status.PENDING
           elif recived_response == "Refused":
              status = Payment_Records.Status.FAILED
           elif recived_response == "Expired":
              status = Payment_Records.Status.FAILED
           elif recived_response == "User canceled":
              messages.error(request,"Order has been cancled !")
              status = Payment_Records.Status.FAILED
           else:
            status = Payment_Records.Status.FAILED
            messages.error(request,'Invalid Payment Session')
            return redirect("home:products_list")
           
           payment_record.service_provider_status = status
           
           payment_record.fee = float(response['fee'])/100
           payment_record.status = status
           payment_record.save()
           
       else:
            messages.error(request,"Missguided payment !")
            return redirect('home:products_list') 
    except Exception as e:
       print(e)
       messages.error(request,"Payment Does not exist")
       return redirect("home:products_list")
    
    if payment_record.status == Payment_Records.Status.COMPLETED and payment_record.service_provider_status == Payment_Records.Status.COMPLETED:
      send_notification_saflora(cart_id=cart_id)
      send_notification_user(cart_id=cart_id)


   
    return redirect("home:products_list") 


# next we need to integrate esewa !
# def esewa_payment(request):
#     amount = "100"
#     tax_amount = "10"
#     total_amount = "110"
#     transaction_uuid = "241028"
#     product_code = "EPAYTEST"
#     secret_key = ""  # UAT secret key
#     success_url = "https://developer.esewa.com.np/success"
#     failure_url = "https://developer.esewa.com.np/failure"
#     signed_field_names = "total_amount,transaction_uuid,product_code"
#     data_to_sign = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
#     signature = base64.b64encode(
#         hmac.new(secret_key.encode(), data_to_sign.encode(), hashlib.sha256).digest()
#     ).decode()

#     context = {
#         "amount": amount,
#         "tax_amount": tax_amount,
#         "total_amount": total_amount,
#         "transaction_uuid": transaction_uuid,
#         "product_code": product_code,
#         "product_service_charge": "0",
#         "product_delivery_charge": "0",
#         "success_url": success_url,
#         "failure_url": failure_url,
#         "signed_field_names": signed_field_names,
#         "signature": signature,
#         "epay_url": "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
#     }
#     return render(request, "payment/esewa.html", context)


