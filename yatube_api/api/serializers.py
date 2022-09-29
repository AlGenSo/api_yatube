from rest_framework import serializers

from posts.models import Post, Group, Comment


class PostSerializer(serializers.ModelSerializer):
    '''Преобразование данных класса Post'''

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Post
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    '''Преобразование данных класса Group'''

    class Meta:
        model = Group
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    '''Преобразование данных класса Comment'''

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)
