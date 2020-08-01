from django.urls import path
from .views import UserCreateAPIView

urlpatterns = [
    path('user/register', UserCreateAPIView.as_view()),
    ]