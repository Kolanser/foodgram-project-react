from django.shortcuts import get_object_or_404
from recipes.models import Follow, Ingredient, Recipe, Tag
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import (
    CustomUser,
    FollowSerializer,
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
    RecipeWriteSerializer
)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Получение ингридиентов."""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class TagViewSet(ReadOnlyModelViewSet):
    """Получение тегов."""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class RecipeViewSet(ModelViewSet):
    """Получение рецептов."""
    queryset = Recipe.objects.all()

    def perform_create(self, serializer): 
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return RecipeWriteSerializer
        return RecipeSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class FollowViewSet(ModelViewSet):
    """Получение подписок."""
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    # def perform_create(self, serializer):
    #     user_id = self.kwargs.get('user_id')
    #     following = get_object_or_404(CustomUser, id=user_id)
    #     serializer.save(user=self.request.user, following=following)

    # @action(methods=['post', 'delete'], detail=True)
    # def subscribe(self, request, pk=None):
    #     following = get_object_or_404(CustomUser, id=pk)
    #     user = request.user
    #     if (self.request.method == 'DELETE' and
    #             user.subscriptions.filter(following=following)):
    #         Follow.objects.filter(
    #             user=request.user, following=following
    #         ).delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     elif (self.request.method == 'POST' and
    #             not user.subscriptions.filter(following=following)):
    #         Follow.objects.create(user=request.user, following=following)
    #         return Response(status=status.HTTP_200_OK)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, )
    # def subscriptions(self, request, pk=None):
    #     pass


from djoser.views import UserViewSet

class CustomUserViewSet(UserViewSet):
    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, pk=None):
        following = get_object_or_404(CustomUser, id=pk)
        user = request.user
        if (self.request.method == 'DELETE' and
                user.subscriptions.filter(following=following)):
            Follow.objects.filter(
                user=request.user, following=following
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif (self.request.method == 'POST' and
                not user.subscriptions.filter(following=following)):
            Follow.objects.create(user=request.user, following=following)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def subscriptions(self, request, pk=None):
        # instance = self.get_object()
        instance = get_object_or_404(Follow, user=request.user)
        # serializer_class_obj = FollowSerializer
        serializer_class_obj = self.get_serializer(instance=instance)
        # serializer_class_obj = FollowSerializer(instance=instance)
        return Response(serializer_class_obj.data)

    # @action(detail=True)
    # def interfaces(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer_obj = self.get_serializer(instance=instance)
    #     return Response(serializer_obj.data)

    def get_serializer_class(self):
        if self.action == 'subscriptions':
            return FollowSerializer
        return self.serializer_class