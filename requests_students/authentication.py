from rest_framework import authentication
from rest_framework import exceptions
import jwt
import jws
from django.conf import settings
import requests


class User:
    def __init__(self, jwt_user):
        self.user = jwt_user
        self.is_authenticated = True


class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise exceptions.AuthenticationFailed('No token')
        else:
            token = token.split(' ')[1]

        key = settings.SECRET_JWT

        try:
            payload = jwt.decode(jwt=token, key=key, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise exceptions.ValidationError('Signature verification failed')

        header = {
            "alg": "HS256",
            "typ": "JWT"
        }
        signature = jws.sign(header, payload, key)

        try:
            jws.verify(header, payload, signature, key)
        except jws.exceptions.SignatureError:
            raise exceptions.ValidationError('Wrong token')

        if payload.get("user_type") == 'student':
            url = 'https://auth.6an.ru/api/user/student'
        else:
            url = 'https://auth.6an.ru/api/user/professor'
        r = requests.post(
            url=url,
            headers={'Authorization': 'Bearer ' + token}
        )

        full_user = r.json()

        user = User(jwt_user=full_user)
        return user, None  # authentication successful
