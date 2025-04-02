from django.urls import path
from .views import (
    RegisterAPIView, VerifyEmailAPIView, EmailLoginAPIView,
    VerifyLoginCodeAPIView, UserProfileAPIView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('login/', EmailLoginAPIView.as_view(), name='login'),
    path('verify-login/', VerifyLoginCodeAPIView.as_view(), name='verify-login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
]
