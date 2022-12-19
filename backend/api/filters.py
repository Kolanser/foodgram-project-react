from django_filters import rest_framework as filters
from django_filters import FilterSet, AllValuesFilter, BooleanFilter, ModelMultipleChoiceFilter, NumberFilter, NumericRangeFilter
from recipes.models import Recipe, Ingredient, Tag

class RecipesFilter(FilterSet):

    is_favorited = NumberFilter(
        method='filter_is_favorited',
    )
    is_in_shopping_cart = NumberFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = AllValuesFilter(
        field_name='tags__slug',
    )
    author = NumberFilter(
        field_name='author__id',
    )

    def get_filter_queryset(self, queryset, value, user, target_sample):
        if user.is_anonymous or value not in (0, 1):
            return queryset
        ids = list(
            target_sample.values_list(
                'recipe__id',
                flat=True
            )
        )
        if value == 1:
            return queryset.filter(id__in=ids)
        return queryset.exclude(id__in=ids)


    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        target_sample = user.favorite_recipes
        return self.get_filter_queryset(queryset, value, user, target_sample)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        target_sample = user.shopping_carts
        return self.get_filter_queryset(queryset, value, user, target_sample)

class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr='startswith'
    )

    class Meta:
        model = Ingredient
        fields = ['name', ]


# class CustumFilter()