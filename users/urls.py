from django.urls import path
from users.views import login

urlpatterns = [
    path('', login.login),
    path('user/login/', login.login, name='user_login'),
    path('user/register/', login.register, name='user_register'),
    path('user/logout/', login.logout, name='user_logout'),
]