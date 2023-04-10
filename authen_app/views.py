import os
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import SignupForm
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from random import randint
from datetime import datetime, timedelta
from accomodation_system import settings
from django.core.mail import send_mail
import re
from .models import CustomUser
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
# Create your views here.


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def check_email(email):
    if re.search(regex, email):
        res = "Valid Email"
    else:
        res = "Invalid Email"
    return res


def check_phone_number(phone_number):
    if phone_number.startswith('+60'):
        res = "Valid Phone Number"
    else:
        res = "Invalid Phone Number"
    return res


@csrf_exempt
def signup_request(request):
    if request.method == 'POST':
        try:
            form = SignupForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                # full_name = request.POST.get('full_name')
                phone_number = request.POST.get('phone_number')
                email = request.POST.get('email')
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    user.phone_number = phone_number
                    user.email = email
                    user.save()
                    user_id = user.id
                    return redirect('login')

                else:
                    error = form.errors
                    print(error)
                    if error == 'password2':
                        print(f"The two password fields did not match.")
                    context = {
                        'status': 'failed',
                        'error': 'There is an issue with saving all info.',
                    }
                    return render(request, 'sign_up.html', context)
            else:
                error = form.errors
                print(error)
                if error == 'password2':
                    print(f"The two password fields did not match.")
                context = {
                    'status': 'failed',
                    'error': error,
                }
                return render(request, 'sign_up.html', context)
        except Exception as e:
            context = {
                'status': 'failed',
                'error': str(e),
            }
            return render(request, 'sign_up.html', context)
    return render(request, 'sign_up.html')



@csrf_exempt
def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error = 'Invalid username or password'
                context = {
                    'status': 'failed',
                    'error': error,
                }
                return render(request, 'login.html', context)
        except Exception as e:
            error = 'Invalid username or password'
            context = {
                'status': 'failed',
                'error': error,
            }
            return render(request, 'login.html', context)
    return render(request, 'login.html')


@csrf_exempt
def logout_request(request):
    logout(request)
    return redirect('login')

# def confirm_email(OTP, email_address):
#     try:
#         subject = 'Thank you for registering to our site'
#         message = 'Here is your OTP to Get Registered on HomeSifu '+'"'+str(OTP)+'"  .' 'This OTP can be used for ' \
#                                                                                  'next 60 minutes.'
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [email_address]
#         send_mail(subject, message, email_from, recipient_list)
#         return True
#     except Exception as e:
#         return str(e)
#
#
# @csrf_exempt
# def verify_account(request):
#     if request.method == 'POST':
#         user_id = request.POST.get("user_id")
#         OTP = request.POST.get("OTP")
#         try:
#             obj_account_data_verified = CustomUser.objects.filter(pk=user_id, is_account_verified=True).exists()
#             if obj_account_data_verified:
#                 context = {
#                     "status": "failed",
#                     "description": "Your account is already verified.",
#                     "Error": ''
#                 }
#                 return JsonResponse(context)
#             else:
#                 obj_account_data_verified = CustomUser.objects.get(pk=user_id)
#                 saved_OTP = obj_account_data_verified.OTP
#                 now = str(datetime.now().strftime('%Y%m%d%H%M%S.%f'))
#                 now_plus_60minutes = str(obj_account_data_verified.OTP_expiration_datetime.strftime('%Y%m%d%H%M%S.%f'))
#                 print("now", now)
#                 print("expiration", now_plus_60minutes)
#                 if now < now_plus_60minutes:
#                     if OTP == saved_OTP:
#                         obj_account_data_verified.is_account_verified = True
#                         obj_account_data_verified.save()
#                         context = {
#                             "status": "ok",
#                             "description": "Your account has been verified successfully.",
#                             "Error": ''
#                         }
#                         return JsonResponse(context)
#                     else:
#                         context = {
#                             "status": "failed",
#                             "description": "Your OTP is wrong and E-mail could not be verified.",
#                             "Error": ''
#                         }
#                         return JsonResponse(context)
#                 else:
#                     context = {
#                         "status": "failed",
#                         "description": "Your OTP has been expired and E-mail could not be verified.",
#                         "Error": ''
#                     }
#                     return JsonResponse(context)
#         except Exception as e:
#             context = {
#                 "status": "failed",
#                 "error": str(e)
#             }
#             return JsonResponse(context)
#     context = {
#         "status": "failed",
#         "error": "Invalid request."
#     }
#     return JsonResponse(context)
#
#
# @csrf_exempt
# def regenerate_OTP_API(request):
#     if request.method == 'POST':
#         user_id = request.POST.get("user_id")
#         OTP = random_with_N_digits(4)
#         try:
#             user = CustomUser.objects.get(pk=user_id)
#         except Exception as e:
#             context = {
#                 "status": "failed",
#                 "description": "No user found.",
#                 "error": str(e)
#             }
#             return JsonResponse(context)
#         email = user.email
#         confirm_email(OTP, email)
#         user.OTP = OTP
#         now = datetime.now()
#         now_plus_60minutes = now + timedelta(minutes=60)
#         user.OTP_generated_datetime = now
#         user.OTP_expiration_datetime = now_plus_60minutes
#         user.save()
#         context = {
#             "status": "success",
#             "description": "Your new OTP has been sent to your E-mail account.",
#             "error": "NO error"
#         }
#         return JsonResponse(context)
#     else:
#         context = {
#             "status": "failed",
#             "description": "",
#             "error": "Invalid request."
#         }
#         return JsonResponse(context)
#
#
# @csrf_exempt
# def userForgotPassword(request):
#     if request.method == 'POST':
#         username = request.POST.get("username")
#         try:
#             user = CustomUser.objects.get(Q(email=username) | Q(phone_number=username))
#             if user:
#                 OTP = random_with_N_digits(4)
#                 email = user.email
#                 password_reset_email(OTP, email)
#                 user.password_reset_OTP = OTP
#                 now = datetime.now()
#                 now_plus_60minutes = now + timedelta(minutes=60)
#                 user.password_reset_request = True
#                 user.password_reset_request_sent_datetime = now
#                 user.password_reset_request_expiration = now_plus_60minutes
#                 user.save()
#                 context = {
#                     "status": "success",
#                     "description": "Your password reset OTP has been sent to your E-mail account.",
#                     "user_id": user.id
#                 }
#                 return JsonResponse(context)
#         except Exception as e:
#             print(e)
#             context = {
#                 "status": "failed",
#                 "description": "No user found against this email / phone .",
#                 "error": str(e)
#             }
#             return JsonResponse(context)
#     else:
#         context = {
#             "status": "failed",
#             "description": "",
#             "error": "Invalid request."
#         }
#         return JsonResponse(context)
#
#
# def password_reset_email(OTP, email_address):
#     try:
#         subject = 'Thank you for registering to our site'
#         message = 'Here is your OTP to change your password on HomeSifu '+'"'+str(OTP)+'".' \
#                                                                                        'This OTP can be used for next '\
#                                                                                        '60 minutes. '
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [email_address]
#         send_mail(subject, message, email_from, recipient_list)
#         return True
#     except Exception as e:
#         return str(e)
#
#
# @csrf_exempt
# def new_password_using_OTP(request):
#     if request.method == 'POST':
#         OTP = request.POST.get('OTP')
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')
#         user_id = request.POST.get('user_id')
#         if new_password == confirm_password:
#             try:
#                 user = CustomUser.objects.get(pk=user_id)
#                 if user:
#                     saved_OTP = user.password_reset_OTP
#                     now = str(datetime.now().strftime('%Y%m%d%H%M%S.%f'))
#                     password_reset_request_expiration = str(
#                         user.password_reset_request_expiration.strftime('%Y%m%d%H%M%S.%f'))
#                     if now < password_reset_request_expiration:
#                         if OTP == saved_OTP and user.password_reset_request:
#                             user.set_password(new_password)
#                             user.password_reset_request = False
#                             user.save()
#                             context = {
#                                 "status": "success",
#                                 "description": "your password has been changed successfully",
#                                 "Error": ''
#                             }
#                             return JsonResponse(context)
#                         else:
#                             context = {
#                                 "status": "failed",
#                                 "description": "Your OTP is wrong and E-mail could not be verified.",
#                                 "Error": ''
#                             }
#                             return JsonResponse(context)
#                     else:
#                         context = {
#                             "status": "failed",
#                             "description": "Your OTP has been expired and E-mail could not be verified.",
#                             "Error": ''
#                         }
#                         return JsonResponse(context)
#             except Exception as e:
#                 print(e)
#                 context = {
#                     "status": "failed",
#                     "description": "No user found against this email / phone .",
#                     "error": str(e)
#                 }
#                 return JsonResponse(context)
#         context = {
#             "status": "success",
#             "description": "Your password reset OTP has been sent to your E-mail account.",
#             "error": "NO error"
#         }
#         return JsonResponse(context)


def numOfDays(date1, date2):
    return (date2 - date1).days
