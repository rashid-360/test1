from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["user_type"] = user.user_type
        token["username"] = user.username

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        request = self.context["request"]  # Get request context
        user = self.user  # The authenticated user

        if request.path == "/api/admin/login/" and user.user_type != "admin":
            raise serializers.ValidationError({"error": "Users cannot log in from the admin route."})
        
        if request.path == "/api/user/login/" and user.user_type != "user":
            raise serializers.ValidationError({"error": "Admins cannot log in from the user route."})

        # Include username and user_type in the response
        data["user_type"] = user.user_type
        data["username"] = user.username  

        return data
