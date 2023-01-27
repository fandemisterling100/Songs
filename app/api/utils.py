import re

from rest_framework import serializers

from app.api.constants import PASSWORD_CHARACTERS, PASSWORD_LENGTH


def password_validator(password):
    if len(password) < PASSWORD_LENGTH:
        message = f"Password must be at least {PASSWORD_LENGTH} characters long"
        raise serializers.ValidationError(message)

    uppercase = bool(re.match(r"\w*[A-Z]\w*", password))
    if not uppercase:
        message = f"Password must have at least one uppercase letter"
        raise serializers.ValidationError(message)

    lowercase = bool(re.match(r"\w*[a-z]\w*", password))
    if not lowercase:
        message = f"Password must have at least one lowercase letter"
        raise serializers.ValidationError(message)

    matches = [character in password for character in PASSWORD_CHARACTERS]
    if not any(matches):
        message = f"The password must contain at least one of the following characters: !, @, #, ? or ]"
        raise serializers.ValidationError(message)
