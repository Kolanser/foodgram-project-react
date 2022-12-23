from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import Follow

from .filters import IngredientFilter, RecipesFilter
from .pagination import PageNumberLimitPagination
from .permissions import IsUserOrReadOnly
from .renderers import PassthroughRenderer
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeReducedSerializer, RecipeSerializer,
                          RecipeWriteSerializer, TagSerializer)

User = get_user_model()


class IngredientViewSet(ReadOnlyModelViewSet):
    """Получение ингридиентов."""

    pagination_class = None
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filterset_class = IngredientFilter
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['name']


class TagViewSet(ReadOnlyModelViewSet):
    """Получение тегов."""
    pagination_class = None
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class RecipeViewSet(ModelViewSet):
    """Получение рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = [IsUserOrReadOnly]
    pagination_class = PageNumberLimitPagination
    filterset_class = RecipesFilter
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = [
        'tags',
        'author',
        'is_favorited',
        'is_in_shopping_cart'
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['favorite', 'shopping_cart']:
            return RecipeReducedSerializer
        if self.request.method in ('POST', 'PATCH'):
            return RecipeWriteSerializer
        return RecipeSerializer

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if (self.request.method == 'DELETE'
                and user.favorite_recipes.filter(recipe=recipe)):
            user.favorite_recipes.get(recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if (self.request.method == 'POST'
                and not user.favorite_recipes.filter(recipe=recipe)):
            Favorite.objects.create(user=user, recipe=recipe)
            serializers_obj = self.get_serializer(
                recipe
            )
            return Response(
                serializers_obj.data,
                status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if (self.request.method == 'DELETE'
                and user.shopping_carts.filter(recipe=recipe)):
            user.shopping_carts.get(recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if (self.request.method == 'POST'
                and not user.shopping_carts.filter(recipe=recipe)):
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializers_obj = self.get_serializer(
                recipe
            )
            return Response(
                serializers_obj.data,
                status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get'],
        detail=False,
        renderer_classes=(PassthroughRenderer,),
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        final_list = {}
        ingredients = IngredientRecipe.objects.filter(
            recipe__in_shopping_cart__user=user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount'
        )
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                final_list[name]['amount'] += item[2]
        response = HttpResponse(str(final_list), content_type='text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.txt"')
        return response


class CustomUserViewSet(UserViewSet):
    """Получение и работа с пользователями."""
    pagination_class = PageNumberLimitPagination

    def get_permissions(self):
        if self.request.user.is_anonymous and (
            self.action in ('me', 'subscribe', 'subscriptions')
        ):
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id=None):
        following = get_object_or_404(User, id=id)
        user = request.user
        if (self.request.method == 'DELETE'
                and user.subscriptions.filter(following=following)):
            Follow.objects.filter(
                user=user, following=following
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if (self.request.method == 'POST'
                and user != following
                and not user.subscriptions.filter(following=following)):
            Follow.objects.create(user=user, following=following)
            serializer_class_obj = self.get_serializer(
                user.subscriptions.get(user=user, following=following)
            )
            return Response(
                serializer_class_obj.data,
                status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_response_data(self, paginated_queryset):
        return self.get_serializer(
            paginated_queryset, many=True
        ).data

    @action(detail=False)
    def subscriptions(self, request):
        queryset = request.user.subscriptions
        page = self.paginate_queryset(queryset.all())
        if page:
            data = self.get_response_data(page)
            return self.get_paginated_response(data)
        data = self.get_response_data(queryset)
        return Response(data)

    def get_serializer_class(self):
        if self.action in ['subscriptions', 'subscribe']:
            return FollowSerializer
        return super().get_serializer_class()
