from django.urls import path

from core.views import *

app_name = 'core'
urlpatterns = [
    path('', about, name='about'),
    path('register/', newRegister, name='register'),
    path('newRegister/', newRegister, name='newRegister'),
    path('register/verifymail', verify_mail, name='verify_mail'),
    path('register/verifyusername', verify_username, name='verify_username'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('accounts/social/signup/', social_register, name='social-register'),
    path('user-verification/', user_verification, name='user-verification'),
]
