from django.urls import path, include
from rest_framework.routers import DefaultRouter

from djx_account.views.login_views import LoginViewSet
from djx_account.views.registration_views import RegistrationViewSet
from djx_account.views.reset_password_views import ResetPasswordViewSet
from djx_account.views.user_confirmation_views import UserConfirmationViewSet
from djx_account.views.user_views import UserViewSet

router = DefaultRouter()
router.register(r'registration', RegistrationViewSet, basename='registration')
router.register(r'login', LoginViewSet, basename='login', )
router.register(r'user', UserViewSet, basename='user')
router.register(r'reset-password', ResetPasswordViewSet, basename='reset-password')
router.register(r'user-confirmation', UserConfirmationViewSet, basename='user-confirmation')

urlpatterns = [
    path('', include(router.urls)),
]
