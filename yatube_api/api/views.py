from rest_framework import viewsets
from rest_framework.views import PermissionDenied
from django.shortcuts import get_object_or_404

from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    '''view-класс реализующий операции модели Post'''

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        '''Создание поста автором'''

        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        '''Изменеие поста автором'''

        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'Изменение чужого поста запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        '''Удаление поста автором'''

        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого поста запрещено!')
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    '''view-класс реализующий операции модели Group'''

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    '''view-класс реализующий операции модели Comment'''

    serializer_class = CommentSerializer

    def get_queryset(self):
        '''Получение всех комментов к посту'''

        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        '''Создание коммента'''

        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        )

    def perform_update(self, serializer):
        '''Изменеие коммента автором'''

        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'Изменение чужого коммента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        '''Удаление коммента автором'''

        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого коммента запрещено!')
        instance.delete()
