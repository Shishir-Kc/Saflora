from Accounts.models import Saflora_user
from .models import Verification_code
from datetime import timedelta
from django.utils import timezone

def does_user_exists(email):
    try:
        user = Saflora_user.objects.get(email=email)
        return True
    except Saflora_user.DoesNotExist:
        return False
    
def is_code_expired(email,code:str):
    """
        To check if the code has expired or not ! 
    
    """
    now = timezone.now()
    try:
        exists = Verification_code.objects.get(email=email,code=code)
        if exists.expires_at < now:
            return False
        else:
            return True 
    except Verification_code.DoesNotExist:
        raise ValueError ("Code Does not Exist !")
        



def is_code_valid(email,code):
    """
        To check if the code is valid or not !
    """
    try:
            user = Saflora_user.objects.get(email=email)
            is_expired = is_code_expired(email=email,code=code)
            if is_expired:
                 return True
            else:
                 return False
    except Saflora_user.DoesNotExist:
            return False
    except Verification_code.DoesNotExist:
            return False
        