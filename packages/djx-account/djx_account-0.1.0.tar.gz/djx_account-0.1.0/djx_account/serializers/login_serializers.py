from django.urls import reverse as reverse_url
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from djx_account.models import UserModel
from djx_account.serializers.base_oauth_serializers import OauthBaseGetUrlLoginSerializer, \
    OauthBaseLoginSerializer
from djx_account.serializers.user_token_serializers import UserTokenSerializer
from djx_account.services.discord_service import DiscordService
from djx_account.services.google_service import GoogleService
from djx_account.services.microsoft_service import MicrosoftService
from djx_account.services.twitter_service import TwitterService
from djx_account.utils.error_messages import ErrorMessage
from djx_account.utils.exceptions import ForbiddenRequestException, BadRequestException
from djx_account.utils.others import OauthCategory


class RefreshSerializer(UserTokenSerializer):
    refresh_token = serializers.CharField()

    def create(self, validated_data):
        refresh = RefreshToken(validated_data["refresh_token"])
        user_id = refresh['user_id']
        user = UserModel.objects.get(id=user_id)
        return user


class LoginSerializer(UserTokenSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        try:
            user = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            raise ForbiddenRequestException(ErrorMessage.username_password_mismatch)
        if not user.check_password(password):
            raise ForbiddenRequestException(ErrorMessage.username_password_mismatch)
        return user


class LoginWithGoogleUrlSerializer(OauthBaseGetUrlLoginSerializer):
    service = GoogleService
    default_redirect_url = 'login-oauth-google'
    oauth_category = OauthCategory.google

class LoginWithGoogleSerializer(OauthBaseLoginSerializer):
    code = serializers.CharField(required=True)

    oauth_category = OauthCategory.google
    service = GoogleService
    default_redirect_url = 'login-oauth-google'



class BaseLoginWithTwitterSerializer(serializers.Serializer):
    redirect_to = serializers.URLField(write_only=True, required=False)

    def get_default_redirect_to_value(self, value):
        if value is None:
            req = self.context['request']
            google_url = reverse_url('login-oauth-twitter')
            value = req.build_absolute_uri(google_url)
        return value


class LoginWithTwitterUrlSerializer(BaseLoginWithTwitterSerializer):
    url = serializers.URLField(read_only=True)
    oauth_state = serializers.JSONField(default={}, write_only=True)

    def create(self, validated_data):
        redirect_to = validated_data.get('redirect_to', None)
        oauth_state = validated_data['oauth_state']
        redirect_to = self.get_default_redirect_to_value(redirect_to)
        url = TwitterService.get_url(redirect_to, oauth_state)
        return {"url": url}


class LoginWithTwitterSerializer(UserTokenSerializer):
    oauth_token = serializers.CharField(required=True)
    oauth_verifier = serializers.CharField()

    def create(self, validated_data):
        oauth_token = validated_data.get('oauth_token')
        oauth_verifier = validated_data.get('oauth_verifier')
        user_info = TwitterService.check_token(oauth_token, oauth_verifier)
        try:
            user = UserModel.objects.get(email=user_info['email'])
        except UserModel.DoesNotExist:
            raise BadRequestException(ErrorMessage.user_not_found)
        return user


class BaseLoginWithMicrosoftSerializer(serializers.Serializer):
    redirect_to = serializers.URLField(write_only=True, required=False)

    def get_default_redirect_to_value(self, value):
        if value is None:
            req = self.context['request']
            google_url = reverse_url('login-oauth-microsoft')
            value = req.build_absolute_uri(google_url)
        return value


class LoginWithMicrosoftUrlSerializer(BaseLoginWithMicrosoftSerializer):
    url = serializers.URLField(read_only=True)
    oauth_state = serializers.JSONField(default={}, write_only=True)

    def create(self, validated_data):
        redirect_to = validated_data.get('redirect_to', None)
        oauth_state = validated_data['oauth_state']
        redirect_to = self.get_default_redirect_to_value(redirect_to)
        url = MicrosoftService.get_url(redirect_to, oauth_state)
        return {"url": url}


class LoginWithMicrosoftSerializer(BaseLoginWithMicrosoftSerializer, UserTokenSerializer):
    code = serializers.CharField(required=True)

    def create(self, validated_data):
        code = validated_data.get('code')
        redirect_to = validated_data.get('redirect_to', None)
        redirect_to = self.get_default_redirect_to_value(redirect_to)
        user_info = MicrosoftService.check_token(code=code, redirect_uri=redirect_to)
        try:
            user = UserModel.objects.get(email=user_info['email'])
        except UserModel.DoesNotExist:
            raise BadRequestException(ErrorMessage.user_not_found)
        return user


class LoginWithDiscordUrlSerializer(OauthBaseGetUrlLoginSerializer):
    service = DiscordService
    default_redirect_url = 'login-oauth-discord'
    oauth_category = OauthCategory.discord


class LoginWithDiscordSerializer(OauthBaseLoginSerializer):
    code = serializers.CharField(required=True)

    oauth_category = OauthCategory.discord
    service = DiscordService
    default_redirect_url = 'login-oauth-discord'

    def post_save(self, user, validated_data, service_response):
        additional_data = service_response['additional_data']
        user.add_claims("discord_guilds", additional_data['discord_guilds'])

