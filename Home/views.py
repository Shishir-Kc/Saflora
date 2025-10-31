from django.shortcuts import render,redirect
from Product.models import Saflora_Product,Saflora_Base_Product
from Accounts.models import Cart,Saflora_user
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# @login_required
def in_home(request):
    return render(request,'Home/Landing_page/landing_page.html')


def base_navbar(request):
    return render(request,'Home/base/navbar.html')

def products_list(request):
   items = Saflora_Base_Product.objects.all()
   print(items)
   context = {
       'items':items
   }
   return render (request,'Home/Products/products.html',context)


def check_out(request,id,cart_id=None):
    user = request.user
    if request.user.is_anonymous:
        user = Saflora_user.objects.get(username='AnonymousUser')
    
    if request.method == "POST":
        payment_method = request.POST.get('payment_method')
        quantity = request.POST.get('quantity_display')
        product_id = request.POST.get("product_id")
        variant = request.POST.get('variant')

        # try:
        print('---------------')
        print(product_id)
        product = Saflora_Product.objects.get(id=product_id)
        if Cart.objects.filter(id=cart_id).exists():
            cart = Cart.objects.get(id=cart_id)
            cart.product = product
            cart.quantity = quantity
            cart.variant = variant
            cart.save()
        else:
         cart = Cart.objects.create(product=product,user=user,cart_status=Cart.Status.IN_CART,quantity=quantity,variant=variant)
        
        if payment_method == "khalti":
            return redirect("payment:Khalti_payment",id=product.id,cart_id=cart.id)
        elif payment_method == "cod":
            return # need to add a proper cod method 
        # except:
            
            # return redirect("home:products_list")
    else:
     print("get")
     item = Saflora_Base_Product.objects.get(id=id)
     products = item.items_variants.all()
     context = {
         'products':products,
        'item':item

     }
     return render (request,'Home/check_out/check_out.html',context)
@login_required
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

@login_required
def cart(request):
    if not request.user.is_authenticated:
        messages.error(request,'Must be loged in !')
        return render('home:in_home')
    user = request.user 
    carts = Cart.objects.filter(user=user,cart_status=Cart.Status.IN_CART)
    context = { 
        'carts':carts
    }
    
    return render(request,'Home/cart/cart.html',context)
@login_required
def update_profile(request):
    if request.method == "POST":
        new_email = request.POST.get('email')
        new_contact = request.POST.get('contact')
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        user = Saflora_user.objects.get(username=request.user)
        user.email = new_email
        user.contact = new_contact
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.save()
        messages.success(request,"updated profile info !")
        return redirect("home:user_profile")
    else:
        messages.error(request,'Something went wrong')
        return redirect("home:user_profile")
@login_required
def update_address(request):
    if request.method == "POST":
        new_address = request.POST.get('address')
        new_address_type = request.POST.get('address_type')
        user = Saflora_user.objects.get(username=request.user)
        user.address = new_address
        user.address_type = new_address_type
        user.save()
        messages.success(request,"Updated Address .")
        return redirect("home:user_profile")
    else:
        messages.error(request,'Something went wrong')
        return redirect("home:user_profile")
    


@login_required
def add_to_cart(request,product_id):

    try:
    
        item = Saflora_Base_Product.objects.get(id=product_id)
        cart = Cart.objects.create(user=request.user,cart_status=Cart.Status.IN_CART,item=item)
        messages.success(request,"Sucessfully Added to your cart !")
        return redirect("home:cart")
    except:
        messages.error(request,"cant add to your cart !")
        return redirect("home:products_list")
  
    
@login_required
def delete_cart(request,id):
    if not request.method == "POST": 
     return redirect("home:user_profle")
    
    try:
        cart = Cart.objects.get(id=id)
        cart.delete()
        return redirect("home:cart")
    except:
        messages.error(request,'Cart does not exists !')
        return redirect("home:cart")
    