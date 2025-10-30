from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from Product.models import Saflora_Product
from Accounts.models import Cart,Saflora_user
from django.contrib import messages


# @login_required
def in_home(request):
    return render(request,'Home/Landing_page/landing_page.html')


def base_navbar(request):
    return render(request,'Home/base/navbar.html')

def products_list(request):
   products = Saflora_Product.objects.all()
   for product in products:
       print(product.id)
   context = {
       'products':products
   }
   return render (request,'Home/Products/products.html',context)


def check_out(request,item_name,id):
    product = Saflora_Product.objects.get(id=id)
    print(product.id)
    if request.method == "POST":
       product = Saflora_Product.objects.get(id=id)
       print(product.id)
       try:
         cart = Cart.objects.create(user=request.user,product=product,cart_status=Cart.Status.IN_CART)
       except:
           print("Guest !")
       print("POST")
    #    print(request.POST.get('quantity'))
       return redirect("payment:Khalti_payment",id=id,cart_id =cart.id)
    
    try:
        product = Saflora_Product.objects.get(name=item_name,id=id)
    except Saflora_Product.DoesNotExist:
        return redirect("home:products_list")
    except:
        return redirect("home:products_list")
     
    
    return render (request,'Home/check_out/check_out.html') 



def user_profile(request):
    try:
        user = Saflora_user.objects.get(username=request.user)
    except Saflora_user.DoesNotExist:
        messages.error(request,"Create an account to view your information !")
        return redirect("login:user_login")
    if not user.address:
        messages.error(request,"Please save Your address before purchasing any product !")
        
    context = {
        'user':user
    }
    return render(request,'Home/profile/profile.html',context=context)

def about_us(request):
    return render(request, 'Home/About_us/about_us.html')

def contact(request):
    return render(request, 'Home/contact/contact.html')

def how_to_use(request):
    return render(request, 'Home/how_to_use/how_to_use.html')