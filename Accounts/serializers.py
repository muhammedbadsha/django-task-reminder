from rest_framework import serializers
from .models import MyUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class UserRegistrationSeri(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'password']

        extra_kwargs = {
                'password': {'write_only': True}  # don’t return password in response
            }
    def create(self, validated_data):
        user = MyUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            # Important: use username=email (because USERNAME_FIELD = 'email')
            user = authenticate(email=email, password=password)

            if user is None:
                raise serializers.ValidationError("Invalid credentials")

            if not user.is_active:
                raise serializers.ValidationError("User is inactive")

        else:
            raise serializers.ValidationError("Both email and password are required")

        data["user"] = user
        return data

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = MyUser.objects.filter(email=email)
        user = authenticate(email=email, password=password)
        
        print(user, 'dddddddddddd')
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "email": user.email,
        }