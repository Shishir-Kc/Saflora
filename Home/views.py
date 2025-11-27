from django.shortcuts import render,redirect
from Product.models import Saflora_Product,Saflora_Base_Product
from Accounts.models import Cart,Saflora_user,Location
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Accounts.models import Province,Location
from .tools import check_address

def in_home(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    
    return render(request,'Home/Landing_page/landing_page.html')

def index_home(request):
   if not request.user.is_authenticated:
    return redirect('home:in_home')
   return render(request,'Home/home/index.html')

def base_navbar(request):
    return render(request,'Home/base/navbar.html')

def products_list(request):
   if request.user.is_authenticated:
      user = Saflora_user.objects.get(username=request.user)
      if not user.address or not user.province:
        messages.error(request,"Please save Your address before purchasing any product !")

   items = Saflora_Base_Product.objects.all()
   context = {
       'items':items
   }
   return render (request,'Home/Products/products.html',context)


def check_out(request,id,cart_id=None,item_id=None):
    user = request.user
    if request.user.is_authenticated:
      user = Saflora_user.objects.get(username=user)
      if not user.address or not user.province:
        return redirect("home:user_profile")
      print(check_address(province_id=user.province.id,area_id=user.location.id))       
      if not check_address(province_id=user.province.id,area_id=user.location.id):
         messages.error(request,'Invalid Location !')
         return redirect("home:user_profile")

    if request.method == "POST":
        payment_method = request.POST.get('payment_method')
        quantity = request.POST.get('quantity_display')
        product_id = request.POST.get("product_id")
        variant = request.POST.get('variant')

        try:
         product = Saflora_Product.objects.get(id=product_id)
         if Cart.objects.filter(id=cart_id).exists():
            cart = Cart.objects.get(id=cart_id)
            cart.product = product
            cart.quantity = quantity
            cart.variant = variant
            if request.user.is_authenticated:
             cart.user = request.user
            cart.save()
         else:
          cart = Cart.objects.create(product=product,cart_status=Cart.Status.IN_CART,quantity=quantity,variant=variant)
          item = Saflora_Base_Product.objects.get(items_variants=product.id)
          cart.item = item
          if request.user.is_authenticated:
           cart.user = request.user
          cart.save()
        
         if payment_method == "khalti":
            cart.payment_method = Cart.Payment_Method.ONLINE
            cart.save()
            return redirect("payment:Khalti_payment",id=product.id,cart_id=cart.id)
         elif payment_method == "cod":
            cart.payment_method = Cart.Payment_Method.COD
            cart.save()
            return redirect("payment:Khalti_payment",id=product.id,cart_id=cart.id)
        
        except:
            
            return redirect("home:products_list")
    else:
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
    if not user.address or not user.province:
        messages.error(request,"Please save Your address / Province before purchasing any product !")

    locations = Location.objects.all()
    provinces = Province.objects.all()
    context = {
        'user':user,
        'provinces':provinces,
        'locations':locations,
        'language':user.language
        
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
        new_area = request.POST.get("area")
        new_province = request.POST.get('province')
        if not check_address(province_id=new_province,area_id=new_area):
            messages.error(request,'Invalid Location')
            return redirect('home:user_profile')
        
        province = Province.objects.get(id=new_province)
        user = Saflora_user.objects.get(username=request.user)
        user.province = province
        user.address = new_address
        user.address_type = new_address_type

        try:
            location = Location.objects.get(id=new_area)
            user.location = location
            user.save()
        except Exception as e:
            print(e)
            messages.error(request,"invalid loaction !")
            return redirect("home:user_profile")
        user.save()
        messages.success(request,"Updated Address .")
        return redirect("home:user_profile")
    else:
        messages.error(request,'Something went wrong')
        return redirect("home:user_profile")
    

@login_required
def update_language_preference(request):
    if request.method == "POST":
        preferred_language = request.POST.get('preferred_language')
        print(preferred_language)
        user = Saflora_user.objects.get(username=request.user)
        if preferred_language == 'ne':
           user.language = Saflora_user.Prefered_Language.NEPALI
        elif preferred_language == 'en':
              user.language = Saflora_user.Prefered_Language.ENGLISH
        messages.success(request,"Language Preference Updated !")
        user.save()
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
    


