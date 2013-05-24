from functools import wraps
from flask import url_for, redirect, json, session
from rauth import OAuth2Service
from rauth.service import process_token_request


class Signonotron2(object):
    def __init__(self, client_id, client_secret):
        self.signon = OAuth2Service(
            client_id=client_id,
            client_secret=client_secret,
            name="backdrop",
            authorize_url="http://signon.dev.gov.uk/oauth/authorize",
            access_token_url="http://signon.dev.gov.uk/oauth/token",
            base_url="http://signon.dev.gov.uk"
        )

    def __redirect_uri(self):
        return url_for("oauth_authorized", _external=True)

    def __json_access_token(self, something):
        return json.loads(something)

    def authorize(self):
        params = {
            "response_type": "code",
            "redirect_uri": self.__redirect_uri()
        }
        return redirect(self.signon.get_authorize_url(**params))

    def exchange(self, code):
        data = dict(
            grant_type='authorization_code',
            redirect_uri=self.__redirect_uri(),
            code=code
        )
        response = self.signon.get_raw_access_token('POST', data=data)
        if response.status_code in [200, 201]:
            access_token, = process_token_request(
                response, self.__json_access_token, 'access_token')
        else:
            access_token = None

        return access_token

    def user_details(self, access_token):
        session = self.signon.get_session(access_token)
        user_details = session.get('user.json').json()
        return user_details, "signin" in user_details["user"]["permissions"]


def protected(f):
    @wraps(f)
    def verify_user_logged_in(*args, **kwargs):
        if not "user" in session:
            return redirect(url_for('oauth_login'))
        return f(*args, **kwargs)
    return verify_user_logged_in