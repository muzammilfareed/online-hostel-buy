from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('userRegister/', views.signup_request, name='signup'),
    path('userLogin/', views.login_request, name='login'),
    path('userLogout/', views.logout_request, name='logout'),
    # path('userOTPVerification/', views.verify_account, name='verify_account'),
    # path('regenerate_OTP/', views.regenerate_OTP_API, name='regenerate_OTP_API'),
    # path('userForgotPassword/', views.userForgotPassword, name='userForgotPassword'),
    # path('new_password_using_OTP/', views.new_password_using_OTP, name='new_password_using_OTP'),
]