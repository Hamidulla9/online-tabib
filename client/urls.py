from django.urls import path
from .views import (
    RegisterAPIView, VerifyEmailAPIView, LoginAPIView, UserProfileAPIView,
    EmailLoginView, SendResetCodeView, VerifyCodeResetPasswordView,
    CategoryListView, DoctorListView, AppointmentCreateView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('verify-email/', VerifyEmailAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('profile/', UserProfileAPIView.as_view()),
    path('email-login/', EmailLoginView.as_view()),
    path('send-reset-code/', SendResetCodeView.as_view()),
    path('verify-reset-code/', VerifyCodeResetPasswordView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('doctors/', DoctorListView.as_view()),
    path('appointments/', AppointmentCreateView.as_view()),
]
