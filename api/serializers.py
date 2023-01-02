from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Posts,Comments

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            "email","username","password"
        ]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class CommentSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)
    post=serializers.CharField(read_only=True)
    class Meta:
        model=Comments
        fields=[
            "comment","user","post","created_date"
        ]
    def create(self, validated_data):
        pos=self.context.get("post")
        usr=self.context.get("user")
        return Comments.objects.create(**validated_data,
        post=pos,
        user=usr)

class PostsSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    posts_comments=CommentSerializer(read_only=True,many=True)
    # like=serializers.CharField(read_only=True)
    class Meta:
        model=Posts
        fields=[
            "id",
            "title",
            "image",
            "user",
            "posts_comments"
            # "like"
        ]
