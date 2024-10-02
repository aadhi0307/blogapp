from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'profile_pic', 'phone_number']

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            profile_pic=validated_data.get('profile_pic'),
            phone_number=validated_data.get('phone_number'),
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    
class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'tags', 'image','user_id']