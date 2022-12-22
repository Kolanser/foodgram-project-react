from django_filters import (
    FilterSet,
    ModelMultipleChoiceFilter,
    NumberFilter,
    CharFilter
)
from recipes.models import Tag


class RecipesFilter(FilterSet):

    is_favorited = NumberFilter(
        method='filter_is_favorited',
    )
    is_in_shopping_cart = NumberFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug'
    )
    author = NumberFilter(
        field_name='author__id',
    )

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(
                favorited__user=self.request.user
            )
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(
                in_shopping_cart__user=self.request.user
            )
        return queryset


class IngredientFilter(FilterSet):
    name = CharFilter(
        lookup_expr='startswith'
    )
