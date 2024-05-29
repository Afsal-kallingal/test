from apps.user_account.models import User
from rest_framework import permissions
import random
from apps.main.functions import get_client_ip,sendSMS
from .models import LoginHistory
import datetime
import requests
from django.conf import settings
from rest_framework.authtoken.models import Token




def validate_email(email):
    try:
        if(User.objects.filter(email=email,email_verified=True).exists()):
            return False
        else:
            return True
    except User.DoesNotExist:
        return True
    except:
        return False

def validate_username(username):
    account = None
    try:
        account = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    if account != None:
        return username
    

# def validate_username(username):
#     try:
#         if(User.objects.filter(username=username).exists()):
#             return False
#         else:
#             return True
#     except User.DoesNotExist:
#         return True
#     except:
#         return False
    
def validate_phone(country_code,phone):
    try:
        if(User.objects.filter(country_code=country_code, phone=phone,phone_verified=True).exists()):
            return False
        else:
            return True
    except User.DoesNotExist:
        return True
    except:
        return False



def get_new_username():
    try:
        last_username = User.objects.all().order_by("date_joined").last().username
        return str(int(last_username) + 1)
    except:
        return "1"

    

def send_phone_otp(country_code,phone,otp):
    # sendSMS(apikey, numbers, sender, message)
    message=str(otp) + " is the OTP to access  " + "Khaf Smart Mahall" + ".\n\nPlease do not share this with anyone"
    return sendSMS("{}{}".format(country_code,phone), message)

def send_email_otp(email,otp):
    
    # sendSMS(apikey, numbers, sender, message)
    print("Your OTP is : " ,str(otp))



def random_password(length):
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    symbols = "@#$&_-()=%*:/!?+."

    string = lower + upper + numbers + symbols
    password = "".join(random.sample(string, length))
    return password


def save_login_history(request,user,login_method):
    LoginHistory.objects.create(
        user = user,
        ip_address=get_client_ip(request),
        login_method = login_method
    )
    user.last_login = datetime.datetime.now()
    user.save()



class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.id and request.user.is_admin:
            return True
        return False





def fetch_user_by_phone(phone):
    r = requests.post(settings.USER_ACCOUNT_API_URL + 'fetch-user-by-phone/', data={
            "phone":phone,
            "api_key":settings.USER_ACCOUNT_GATEWAY_KEY,
        })
    return(r.json())



def fetch_user_by_token(token):
    r = requests.post(settings.USER_ACCOUNT_API_URL + 'fetch-user-by-token/', data={
            "token":token,
            "api_key":settings.USER_ACCOUNT_GATEWAY_KEY,
        })
    data = r.json()
    token = update_user_token(data)
    return(token)



def update_user_token(data):
    print("/////////////    data /////////", data)
    user = User.objects.filter(username=data["username"])
    if(user.exists()):
        user.update(
            full_name = data["full_name"],
            email = data["email"],
            phone = data["phone"],
            is_active = data["is_active"],
            is_admin = data["is_admin"],
            is_superuser = data["is_superuser"],
            is_staff = data["is_staff"],
        )
        user = user.first()
        Token.objects.filter(user=user).delete()
    else:
        user=User.objects.create(
            full_name = data["full_name"],
            username = data["username"],
            email = data["email"],
            phone = data["phone"],
            is_active = data["is_active"],
            is_admin = data["is_admin"],
            is_superuser = data["is_superuser"],
            is_staff = data["is_staff"]   
        )
    Token.objects.filter(key=data["token"]).delete()
    token = Token.objects.create(user=user,key=data["token"])
    return {'token':token,'user':user}


def register_user_by_phone(data):
    r = requests.post(settings.USER_ACCOUNT_API_URL + 'register-user-by-phone/', data={
            "phone":data["phone"],
            "email":data["email"],
            "username":data["username"],
            "email":data["email"],
            "api_key":settings.USER_ACCOUNT_GATEWAY_KEY,
        })
    return(r.json())


def set_user_token(user,token):
    Token.objects.filter(user=user).delete()
    Token.objects.filter(key=token).delete()
    token = Token.objects.create(user=user,key=token).key
    return token


def delete_user_token(token):
    r = requests.post(settings.USER_ACCOUNT_API_URL + 'delete-token/', data={
            "token":token,
            "api_key":settings.USER_ACCOUNT_GATEWAY_KEY
        })
    return(r.json())