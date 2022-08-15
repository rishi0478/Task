from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from django.contrib.auth.models import User

class User_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','password']
        # fields = '__all__')

    def create(self, validated_data):
        user = User.objects.create(username= validated_data['username'],email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

