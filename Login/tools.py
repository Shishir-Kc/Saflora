from Accounts.models import Saflora_user

def does_user_exists(email=''):
    try:
        user = Saflora_user.objects.get(email=email)
        return True
    except Saflora_user.DoesNotExist:
        return False