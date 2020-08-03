from django.urls import path

from .views import UserCreateAPIView, ObtainTokenAPI, \
    RefreshTokenAPI

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('token/', ObtainTokenAPI.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenAPI.as_view(),
         name='token_refresh'),
]
