from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Модель пользователя."""
    first_name = models.CharField('first name', max_length=150, unique=True)
    last_name = models.CharField('last name', max_length=150, unique=True)
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class Follow(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь',
        help_text='Пользователь, который подписывается'
    )
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецепта',
        help_text='Автор, на которого подписываются'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                name='unique_follows',
                fields=['user', 'following'],
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='non_self_follow'
            )
        ]
