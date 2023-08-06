import datetime

import requests
from django.utils.timezone import now

from djx_account import settings

try:
    from google.auth.transport import requests as google_request
    from google.oauth2 import id_token
except ModuleNotFoundError:
    pass

from djx_account.utils.error_messages import ErrorMessage
from djx_account.utils.exceptions import BadRequestException


class GoogleService:

    @staticmethod
    def get_url(redirect_uri):
        client_id = settings.GOOGLE_CLIENT_ID
        base_url = "https://accounts.google.com/o/oauth2/auth"
        req = requests.PreparedRequest()
        req.prepare_url(base_url,
                        {"client_id": client_id,
                         "redirect_uri": redirect_uri,
                         "scope": "email",
                         "response_type": "code"})
        return req.url

    @staticmethod
    def check_token(code, redirect_uri):
        response = requests.post(
            url="https://oauth2.googleapis.com/token",
            data={"code": code, "client_id": settings.GOOGLE_CLIENT_ID,
                  "redirect_uri": redirect_uri,
                  "client_secret": settings.GOOGLE_CLIENT_SECRET,
                  "grant_type": "authorization_code"},
        )
        if response.status_code != 200:
            raise BadRequestException(ErrorMessage.invalid_code)

        data = response.json()
        token = data['id_token']
        token_data = id_token.verify_oauth2_token(token, google_request.Request(), clock_skew_in_seconds=0)
        expires_in = token['expires_in']
        expires_at = now() + datetime.timedelta(seconds=expires_in)
        return {
            "user": {
                "email": token_data["email"],
            },
            "credentials": {
                "access_token": data['access_token'],
                "expires_at": expires_at,
            },
            "additional_data": {
                "email_verified": token_data["email_verified"]
            }
        }
