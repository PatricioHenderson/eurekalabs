
from django.contrib.auth.models import User
from rest_framework import serializers



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields= ("username" , "last_name" , "email")

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ("username" , "last_name" , "email" )
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth import get_user_model

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ('username','last_name','email')
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'last_name',
            'email',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)