
from Accounts.models import Cart

def send_notification_saflora(cart_id):
    from Login.tasks import send_purchase_notification_saflora
    address_type = None
    province = None
    postal_code = None
    email = None
    try:
        user_cart = Cart.objects.get(id=cart_id)
        if user_cart.user:
            user = user_cart.user
            user_full_name = user.get_full_name()
            address = user.address
            location = user.location
            address_type = user.address_type
            email = user.email
            contact = user.contact
        else:
            user_full_name = user_cart.anonymous_user.full_name
            address = user_cart.anonymous_user.shipping_address
            location = user_cart.anonymous_user.city
            province = user_cart.anonymous_user.province
            postal_code = user_cart.anonymous_user.postal_code
            email = user_cart.anonymous_user.email
            contact = user_cart.anonymous_user.contact_number
        if user_cart.product.discount_price:
            price = user_cart.product.discount_price
        else:
            price = user_cart.product.price
        message =f"""
            Info:
            
            Customer Name = > {user_full_name},
            Email = > {email},
            Contact = > {contact},

            Item: 

            Base Product = > {user_cart.item}
            Item = > {user_cart.product}
            Quantity = > {user_cart.quantity}
            Item Price = > {price}
            Item Aadded In Cart At = > {user_cart.added_at} 
            
            Payment : 

            Payment Method = >  {user_cart.payment_method}
            Paid Price = > {user_cart.paid_price}
            Total Price = {user_cart.total_price}

            Location : 

            address = > {address}
            location = > {location}
            address_type = > {address_type}
            province = > {province}
            postal code = > {postal_code} 



"""
        data = {
    "Info": {
        "Customer_Name": user_full_name,
        "Email": email,
        "Contact": contact
    },
    "Item": {
        "Base_Product": str(user_cart.item),
        "Item": str(user_cart.product),
        "Quantity": user_cart.quantity,
        "Item_Price": price,
        "Item_Added_In_Cart_At": user_cart.added_at.isoformat()
    },
    "Payment": {
        "Payment_Method": user_cart.payment_method,
        "Paid_Price": user_cart.paid_price,
        "Total_Price": user_cart.total_price
    },
    "Location": {
        "Address": str(address),  # if this is a model
        "Location": str(location),  # convert model instance to string
        "Address_Type": address_type,
        "Province": province,
        "Postal_Code": postal_code
    }
}



        send_purchase_notification_saflora.delay(message,data=data)
        print("Triggering notification for cart", cart_id)
    except Exception as e:
        print("------------------------------------------ ERROR ---------------------------------------")
        print(e)



def send_notification_user(cart_id):
    from Login.tasks import send_order_confirmation
    try:
        user_cart = Cart.objects.get(id=cart_id)
        if user_cart.user:
            user_in = user_cart.user
            user = user_in.get_full_name()
            email = user_in.email

        else:
            user = user_cart.anonymous_user.full_name
            email = user_cart.anonymous_user.email


        send_order_confirmation.delay(customer_email=email,customer_name=user,order_date=user_cart.added_at,cart_id=user_cart.id,total=user_cart.total_price)
        
    except Exception as e:
        print("----------------------Error---------------------")
        print(e)
        return None