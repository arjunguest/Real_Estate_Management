from rest_framework import serializers
from dashboard.models import AiUser, Lease, Tenant, Unit
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiUser
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        User = AiUser(**validated_data)
        User.set_password(password)
        User.save()
        return User

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lease
        fields = "__all__"

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'