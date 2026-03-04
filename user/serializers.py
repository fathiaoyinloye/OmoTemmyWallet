from rest_framework import serializers

from user.models import User
from rest_framework_simplejwt.serializers import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'username']
        extra_kwargs = {'password': {'write_only': True}}



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Incorrect email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect email or password")

        if not user.is_active:
            raise serializers.ValidationError("User account as been disabled")

        refresh = RefreshToken.for_user(user)
        data = {
            "user": user.id,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        return data
