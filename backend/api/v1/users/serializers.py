from rest_framework import serializers

from users.models import User

from .validators import username_me


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор кастомной модели пользователя."""

    username = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r'^[\w.@+-]'
    )

    class Meta:
        abstract = True
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password'
        )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует'
            )
        return username_me(value)


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор токена. Проверяет наличие username."""

    username = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r'^[\w.@+-]'
    )

    class Meta:
        model = User
        fields = ('username', )

    def validate_username(self, data):
        username = data.get('username')
        if not username:
            raise serializers.ValidationError(
                f'Поле {username} не должно быть пустым'
            )
        return data
