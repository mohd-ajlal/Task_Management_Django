from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length = 8)
    password2 = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password2"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def validate_email(self, value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username = value).exists():
            raise serializers.ValidationError("Username is already in use.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def validate(self, data):
        if "password" in data and "password2" in data:
            if data["password"] != data["password2"]:
                raise serializers.ValidationError("Passwords do not match.")
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("password", None)  # Remove password from the representation
        return representation