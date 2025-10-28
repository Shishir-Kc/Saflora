from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from Product.models import Saflora_Product
from Accounts.models import Cart
from django.contrib import messages


# @login_required
def in_home(request):
    return render(request,'Home/Landing_page/landing_page.html')


def base_navbar(request):
    return render(request,'Home/base/navbar.html')

def products_list(request):
   products = Saflora_Product.objects.all()
   context = {
       'products':products
   }
   return render (request,'Home/Products/products.html',context)


def check_out(request,item_name,id):
    if request.method == "POST":
       product = Saflora_Product.objects.get(id=id)
       cart = Cart.objects.create(user=request.user,product=product,cart_status=Cart.Status.IN_CART)
       print("POST")
       print(request.POST.get('quantity'))
       return redirect("payment:Khalti_payment",id=id,cart_id =cart.id)
    try:
        product = Saflora_Product.objects.get(name=item_name,id=id)
    except Saflora_Product.DoesNotExist:
        return redirect("home:products_list")
    except:
        return redirect("home:products_list")
    context = {
        'product':product
    }
     
    
    return render (request,'Home/payment/payment.html',context) 