from django.urls import path
from .views import RegisterView, VerifyCodeView, UserEducationViewSet, AdditionalUniversityViewSet, UserEducationList, \
    ExperienceViewSet, ExperienceList, Extra_workViewSet, LoginView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify/", VerifyCodeView.as_view(), name="verify"),
    path("eduction/", UserEducationViewSet.as_view(), name="verify"),
    path("eductionlist/", UserEducationList.as_view(), name="verify"),
    path("additional/", AdditionalUniversityViewSet.as_view(), name="verify"),
    path("experience/", ExperienceViewSet.as_view(), name="verify"),
    path("experiencelist/", ExperienceList.as_view(), name="verify"),
    path("extra_work/", Extra_workViewSet.as_view(), name="verify"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),

]
