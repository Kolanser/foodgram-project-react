from django.shortcuts import get_object_or_404
from recipes.models import (
    Favorite,
    Follow,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .pagination import PageNumberLimitPagination
from .permissions import IsUserOrReadOnly
from .serializers import (
    CustomUser,
    RecipeReducedSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
    RecipeWriteSerializer
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from djoser.views import UserViewSet


class IngredientViewSet(ReadOnlyModelViewSet):
    """Получение ингридиентов."""

    pagination_class = None
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['favorite', 'shopping_cart']:
            return RecipeReducedSerializer
        elif self.request.method in ('POST', 'PATCH'):
            return RecipeWriteSerializer
        return RecipeSerializer

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if (self.request.method == 'DELETE' and
                user.favorite_recipes.filter(recipe=recipe)):
            user.favorite_recipes.get(recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif (self.request.method == 'POST' and
                not user.favorite_recipes.filter(recipe=recipe)):
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
        if (self.request.method == 'DELETE' and
                user.shopping_carts.filter(recipe=recipe)):
            user.shopping_carts.get(recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif (self.request.method == 'POST' and
                not user.shopping_carts.filter(recipe=recipe)):
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializers_obj = self.get_serializer(
                recipe
            )
            return Response(
                serializers_obj.data,
                status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(UserViewSet):
    """Получение и работа с пользователями."""
    pagination_class = PageNumberLimitPagination

    def get_permissions(self):
        if self.request.user.is_anonymous and (
            self.action == 'me' or
            self.action == 'subscribe' or
            self.action == 'subscriptions'
        ):
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id=None):
        following = get_object_or_404(CustomUser, id=id)
        user = request.user
        if (self.request.method == 'DELETE' and
                user.subscriptions.filter(following=following)):
            Follow.objects.filter(
                user=user, following=following
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif (self.request.method == 'POST' and
                user != following and
                not user.subscriptions.filter(following=following)):
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
        data = self.get_serializer(
            paginated_queryset, many=True
        ).data
        return data

    @action(detail=False)
    def subscriptions(self, request):
        # serializer_class_obj = self.get_serializer(
        #     request.user.subscriptions, many=True
        # )
        # return Response(serializer_class_obj.data)
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


    # def registros_data_table(self, request):
    # queryset = Interfaces.objects.all()

    # page = self.paginate_queryset(queryset)
    # if page is not None:
    #     data = self.get_response_data(page)
    #     return self.get_paginated_response(data)

    # data = self.get_response_data(queryset)
    # return Response(data)
    
    # queryset = Interfaces.objects.all()

    # page = self.paginate_queryset(queryset)
    # if page is not None:
    #     data = self.get_response_data(page)
    #     return self.get_paginated_response(data)

    # data = self.get_response_data(queryset)
    # return Response(data)