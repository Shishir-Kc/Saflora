from django.core.mail import send_mail
from celery import shared_task
from .models import Verification_code
from django.utils import timezone

@shared_task
def send_verification_email(email, code):
    subject = 'Your Verification Code'
    message = f'Your verification code is: {code}'
    from_email = 'test@gmail.com'
    recipient_list = email
    send_mail(subject, message, from_email, recipient_list)
    print("Email sent to ", email)
    return True

@shared_task
def send_purchase_notification_saflora():
    subject = 'Product Pruchased ! '
    message = f'congrats  got 1 order '
    from_email = 'test@gmail.com'
    recipient_list = ['kcmr925@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
    print("Email sent to ", 'kcmr925@gmail.com')
    return True

@shared_task
def clean_used_otps():
    """
        Deletes Used and expired otp 

    """
    now = timezone.now()
    deleted,_ =  Verification_code.objects.filter(is_used= True).delete()
    expired, _ = Verification_code.objects.filter(expires_at__lt =now).delete()
    print(f"deleted {deleted} + {expired} opt(s)")
