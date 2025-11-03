from django.core.mail import send_mail
from celery import shared_task
from .models import Verification_code
from django.utils import timezone
from Accounts.models import Saflora_user
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from email.mime.image import MIMEImage
import os
from django.conf import settings
from Product.models import Saflora_Product,Saflora_Base_Product
from Accounts.models import Cart
from Payment.models import Payment_Records
from dotenv import load_dotenv
import logging
import json
import requests
logger = logging.getLogger(__name__)
from Payment.views import send_notification_saflora , send_notification_user
load_dotenv()


@shared_task
def send_verification_email(email, code,url=None):
   print(email)
   try: 
    user = Saflora_user.objects.get(email=email)
    subject = 'Your Verification Code'
    from_email ='Saflora@gmail.com'
    to = [email]
    message = f'Your verification code is: {code}'
    html_content = render_to_string(
        'reset_pass/send_email.html',
        {
            'user_name':user.get_full_name(),
            'otp_code':code,
            'verification_link':url
        }
    )
    msg = EmailMultiAlternatives(subject, message, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    logo_path = os.path.join(settings.BASE_DIR, 'Login', 'static','Login','images', 'saflora.png')  
    with open(logo_path, 'rb') as f:
        logo = MIMEImage(f.read())
        logo.add_header('Content-ID', '<logo>')
        logo.add_header('Content-Disposition', 'inline', filename='saflora.png')
        msg.attach(logo)
    msg.send()
   except Exception as e:
     print(e)


@shared_task
def send_purchase_notification_saflora(message,data):
    try:
        admin_emails = []
        admins = Saflora_user.objects.filter(is_staff=True)
        if not admins.exists():
            send_mail(
                subject='No Admin found!',
                message='No admin found in Saflora page!',
                from_email='noreply@gmail.com',
                recipient_list=['kc.dev.py@gmail.com']
            )
            return

        for admin in admins:
            admin_emails.append(admin.email)

        html_content = render_to_string(
        'payment/order_alert.html',
        {
          'customer_name': data["Info"]["Customer_Name"],
          'customer_email': data["Info"]["Email"],
          'customer_contact': data["Info"]["Contact"],

          # Item
          'item_name': data["Item"]["Item"],
          'base_product': data["Item"]["Base_Product"],
          'quantity': data["Item"]["Quantity"],
          'item_price': data["Item"]["Item_Price"],
          'item_added_at': data["Item"]["Item_Added_In_Cart_At"],

          # Payment
          'payment_method': data["Payment"]["Payment_Method"],
          'paid_price': data["Payment"]["Paid_Price"],
          'total_price': data["Payment"]["Total_Price"],

          # Location
          'address': data["Location"]["Address"],
          'location': data["Location"]["Location"],
          'address_type': data["Location"]["Address_Type"],
          'province': data["Location"]["Province"],
          'postal_code_': data["Location"]["Postal_Code"],

          'current_year': datetime.now().year,
        }
        )
        text_content = f""" 
            {message}
        """

        from_email = 'Saflora@gmail.com'
        to = admin_emails
        subject = "🚨 🚨 🚨 Order Alert 🚨 🚨 🚨"
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        logo_path = os.path.join(settings.BASE_DIR, 'Payment', 'static', 'assets', 'saflora.png')  
        with open(logo_path, 'rb') as f:
         logo = MIMEImage(f.read())
         logo.add_header('Content-ID', '<logo>')
         logo.add_header('Content-Disposition', 'inline', filename='saflora.png')
         msg.attach(logo)
         msg.send()


    except Exception as e:
        print('Error sending purchase notification:', e)
        import traceback; print(traceback.format_exc())
        return False



@shared_task
def send_order_confirmation(customer_email, customer_name,order_date,cart_id,total):
   try: 
    subject = "Order Confirmation"
    from_email = "Saflora@gmail.com"
    to = [customer_email]

    # Plain text fallback (for email clients that don't support HTML)
    text_content = f"""
    Dear {customer_name},

    Thank you for shopping with us! Your order has been successfully placed.
    We will notify you once it is ready for dispatch.

    For questions, contact us at saflora.nepal@gmail.com.
    """

    # Render the HTML template
    html_content = render_to_string(
        'payment/confirmation.html',
        {
            'customer_name': customer_name,
            'current_year': datetime.now().year,
            'order_date':order_date,
            'order_number':cart_id,
            'order_total':total,
        }
    )

    # Create email
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    logo_path = os.path.join(settings.BASE_DIR, 'Payment', 'static', 'assets', 'saflora.png')  
    with open(logo_path, 'rb') as f:
        logo = MIMEImage(f.read())
        logo.add_header('Content-ID', '<logo>')
        logo.add_header('Content-Disposition', 'inline', filename='saflora.png')
        msg.attach(logo)
    msg.send()
   except Exception as e:
        print("-----------------error------------")
        print(e)

@shared_task
def clean_used_otps():
    """
        Deletes Used and expired otp 

    """
    now = timezone.now()
    deleted,_ =  Verification_code.objects.filter(is_used= True).delete()
    expired, _ = Verification_code.objects.filter(expires_at__lt =now).delete()
    print(f"deleted {deleted} + {expired} opt(s)")


@shared_task
def verify_payment_statements():
  try: 
   khalti_key = os.environ.get("KHALTI_SECRET_KEY")
   base_url = os.environ.get("KHALTI_BASE_URL")
   verify_endpoint = os.environ.get("KHALTI_PAYMENT_VERIFICATION")
   if not all([khalti_key, base_url, verify_endpoint]):
     logger.error("Missing Khalti configuration in environment variables.")
     return
   now = timezone.now()
   records = Payment_Records.objects.filter(status=Payment_Records.Status.INITIATED,payment_method=Payment_Records.Payment_Method.ONLINE,payment_session__lt=now)
   if not records.exists():
        logger.info("No expired initiated payments found.")
        return 
   for record in records:
        pidx = record.pidx
        payment_record = record
        cart = payment_record.cart
        url  =f'{base_url}{verify_endpoint}'
        payload = json.dumps({
        'pidx':pidx
        })
        headers = {
        'Authorization':f'key {khalti_key}',
        'Content-Type':'application/json'
        }
        try: 
           response = requests.request("POST",url=url,data=payload,headers=headers,timeout=5)
        except:
           logging.warning("failed to fetch data")

        try:
          received_response = response.json()
        except ValueError:
         logging.warning(f"Invalid JSON response for payment {pidx}")
         continue
        status_received = received_response['status']
        received_amount = received_response['total_amount']
        print("------------Status from Khalti-----------------------")
        if status_received == "Completed":
            status = Payment_Records.Status.COMPLETED
            send_notification_saflora(cart_id=cart.id)
            send_notification_user(cart_id=cart.id)
        elif status_received == "Pending":
              status = Payment_Records.Status.PENDING
        elif status_received == "Refused":
              status = Payment_Records.Status.FAILED
        elif status_received == "Expired":
              status = Payment_Records.Status.FAILED
        elif status_received == "User canceled":
              status = Payment_Records.Status.FAILED
        else:
            status = Payment_Records.Status.FAILED

        payment_record.service_provider_status = status
        payment_record.fee = float(received_response['fee'])/100
        payment_record.status = status
        payment_record.transaction_id = received_response['transaction_id']
        payment_record.payment_method = Payment_Records.Payment_Method.ONLINE
        cart.paid_price = (float(received_amount)/100) + float(received_response['fee'])/100
        cart.cart_status = Cart.Status.PURCHASED
        cart.save()
        payment_record.save()
           
 
  except Exception as e:
    logging.warning(f"Payment verification task error: {e}")