from rest_framework import authentication
from rest_framework import exceptions
import jwt
import jws
from django.conf import settings


class User:
    def __init__(self, jwt_user):
        self.full_user = jwt_user

        self.id = jwt_user.get('id')
        self.name = f'{jwt_user["first_name"]} {jwt_user["last_name"]}'
        if jwt_user.get("middle_name") is not None:
            self.name += f' {jwt_user.get("middle_name")}'
        self.birthday = jwt_user.get('birthday')
        self.login = jwt_user.get('login')
        self.email = jwt_user.get('email')
        self.phone = jwt_user.get('phone')
        self.about = jwt_user.get('about')
        self.user_type = jwt_user.get('user_type')

        self.is_authenticated = True


class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise exceptions.AuthenticationFailed('No token')
        else:
            if 'bearer' in token.lower():
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

        user = User(jwt_user=payload)

        return user, None  # authentication successful
