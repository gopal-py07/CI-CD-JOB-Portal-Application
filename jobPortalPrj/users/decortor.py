
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import get_user_model

from .models import CustomUser

# user = get_user_model()
# print('line  9--', user)

def is_candidate(CustomUser):
    
    if CustomUser.is_authenticated and (CustomUser.account_type == 'candidates'):
        return True
    else:
        return False
    
    
def is_recruiter(CustomUser):
    
    try:
        if CustomUser.is_authenticated and CustomUser.account_type == 'recruiter':
            return True
    except:
        return False
    
    
    
    
def check_ac_type_candidates_or_recruiter(CustomUser):
    
    if CustomUser.is_authenticated and (CustomUser.account_type == 'candidates' or CustomUser.account_type == 'recruiter'):
        return True
    else:
        return False