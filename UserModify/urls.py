from django.urls import path
from .views import *

#Url pathways to hell

urlpatterns = [
    path('signup/', UserVoidSignupView.as_view(), name='user-signup'),
    path('signin/', UserVoidLoginView.as_view(), name='user-login'),
    path('signout/', UserVoidLogoutView.as_view(), name='user-logout'),
]
