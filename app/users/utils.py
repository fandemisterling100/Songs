from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken

from django.contrib.auth import get_user_model

User = get_user_model()


def decode_simple_jwt_token(request):
    try:
        jwt_object = JWTAuthentication()
        header = jwt_object.get_header(request)
        raw_token = jwt_object.get_raw_token(header)
        validated_token = jwt_object.get_validated_token(raw_token)
        return validated_token
    except (AttributeError, InvalidToken, AuthenticationFailed):
        return {}


def get_user(request):
    user = None
    request_data = decode_simple_jwt_token(request)
    try:
        user_id = request_data.get("user_id", None)
        user = User.objects.get(id=user_id)
    except Exception:
        pass
    return user
