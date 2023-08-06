import json
from collections import OrderedDict

try:
    import msal
except ModuleNotFoundError:
    pass
from djx_account import settings

from djx_account.services.oauth_service_interface import OauthServiceInterface
from djx_account.utils.error_messages import ErrorMessage
from djx_account.utils.exceptions import BadRequestException


class MicrosoftService(OauthServiceInterface):

    @staticmethod
    def get_url(redirect_uri, oauth_state):
        app = msal.ConfidentialClientApplication(
            client_id=settings.MICROSOFT_CLIENT_ID,
            client_credential=settings.MICROSOFT_SECRET
        )
        data = {
            'scopes': ['email'], 'redirect_uri': redirect_uri
        }
        if oauth_state:
            data['state'] = json.dumps(OrderedDict(oauth_state))
        url = app.get_authorization_request_url(**data)
        return url

    @staticmethod
    def check_token(code, redirect_uri):
        app = msal.ConfidentialClientApplication(
            client_id=settings.MICROSOFT_CLIENT_ID,
            client_credential=settings.MICROSOFT_SECRET
        )
        data = {
            'code': code,
            'scopes': ['email'], 'redirect_uri': redirect_uri
        }
        result = app.acquire_token_by_authorization_code(**data)
        try:
            claims = result['id_token_claims']
        except KeyError:
            raise BadRequestException(detail=ErrorMessage.invalid_code)
        email = claims['email'] if 'email' in claims else None
        return {
            "email": email
        }
