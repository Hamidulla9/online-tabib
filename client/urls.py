from django.urls import path
from .views import (
    RegisterAPIView, VerifyEmailAPIView,
    UserProfileAPIView, EmailLoginView,
    SendResetCodeView, VerifyCodeResetPasswordView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('login/', EmailLoginView.as_view(), name='email-login'),
    path('forgot-password/', SendResetCodeView.as_view(), name='forgot-password'),
    path('reset-password/', VerifyCodeResetPasswordView.as_view(), name='reset-password'),
]