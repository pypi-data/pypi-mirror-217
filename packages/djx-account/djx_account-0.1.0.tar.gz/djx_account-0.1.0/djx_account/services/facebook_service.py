import json
from collections import OrderedDict

import facebook

from djx_account import settings
from djx_account.services.oauth_service_interface import OauthServiceInterface


class FacebookService(OauthServiceInterface):

    @staticmethod
    def get_url(redirect_uri, oauth_state):
        data = {
            'app_id': settings.FACEBOOK_CLIENT_ID,
            # 'canvas_url': settings.CLIENT_CHALLENGE_ROUTE,
            'perms': ['email', 'public_profile']
        }
        if oauth_state:
            data['state'] = json.dumps(OrderedDict(oauth_state))

        url = facebook.GraphAPI().get_auth_url(
            **data
        )
        return url

    @staticmethod
    def check_token(code, redirect_uri):
        api = facebook.GraphAPI().get_access_token_from_code(
            code, redirect_uri,
            settings.FACEBOOK_CLIENT_ID,
            settings.FACEBOOK_SECRET)
        access_token = api['access_token']
        me = facebook.GraphAPI(access_token=access_token).get_object('me', **{"fields": 'email,id'})
        user_id = me["id"]
        user_mail = me['email'] if 'email' in me else None
        return {
            **me
        }
