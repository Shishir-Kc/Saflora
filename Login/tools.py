from django.core.mail import send_mail
from Accounts.models import Saflora_user

def send_verification_email(email, code):
    subject = 'Your Verification Code'
    message = f'Your verification code is: {code}'
    from_email = 'test@gmail.com'
    recipient_list = email
    send_mail(subject, message, from_email, recipient_list)
    print("Email sent to ", email)
    return True
    

def does_user_exists(email=''):
    try:
        user = Saflora_user.objects.get(email=email)
        return True
    except Saflora_user.DoesNotExist:
        return False