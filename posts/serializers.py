from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model


# 기본 serializer
class PostBaseSerializer(serializers.Serializer): #기본 serializer
    image = serializers.ImageField(required=False)
    content = serializers.CharField()
    created_at = serializers.DateTimeField(required=False)
    view_count = serializers.IntegerField()
    writer = serializers.IntegerField()
    bad_post = serializers.BooleanField()

    # create 추가
    def create(self, validated_data):
        print(get_user_model().objects.all())
        post = Post.objects.create(
            content = validated_data['content'],
            view_count = validated_data['view_count'],
            writer = User.objects.get(id=validated_data['writer']),
        )
        return post

# ModelSerializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__' # fields = ['id', 'contents']

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
