from allauth.utils import generate_unique_username
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken

from app.api.utils import password_validator
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from app.api.models import Song

User = get_user_model()


class UserTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        validators=[password_validator],
    )
    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def validate(self, data):
        email = data.get("email")
        user = User.objects.filter(email=email)

        if not user.exists():
            raise serializers.ValidationError(
                {
                    "email": [
                        f"The user with email {email} does not exist, please register first."
                    ]
                }
            )

        authenticate_kwargs = {
            "email": data.get("email"),
            "password": data.get("password"),
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass
        self.user = authenticate(**authenticate_kwargs)
        if not self.user:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        return {}


class UserLoginSerializer(UserTokenSerializer):
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        token["user_id"] = user.id
        token["user_username"] = user.username
        token["email"] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, required=True, validators=[password_validator]
    )
    username = serializers.CharField(
        read_only=True,
        required=False,
    )

    class Meta:
        model = User
        fields = ["email", "password", "username"]

    def validate(self, data):
        email = data.get("email")
        user = User.objects.filter(email=email)

        if user.exists():
            raise serializers.ValidationError(
                {"email": [f"The email '{email}' is not available."]}
            )
        return data

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        validated_data["username"] = generate_unique_username(
            [validated_data["email"], "user"]
        )
        return super(UserRegisterSerializer, self).create(validated_data)

        
class SongSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Song
        fields = [
            "pk",
            "name",
            "artist",
            "album",
            "duration",
            "favorite",
            "private",
            "created_by",
        ]