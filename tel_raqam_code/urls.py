# tel_raqam_code/urls.py
from django.urls import path
from .views import VerifyCodeView

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyCodeView.as_view(), name='verify'),
]