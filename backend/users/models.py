from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint


class User(AbstractUser):

    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True,
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='uq_username_email'
            ),
        ]

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="подписчик"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name='автор'
    )

    class Meta:
        verbose_name = 'подписки'
        verbose_name_plural = 'подписки'
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='uq_user_author'
            ),
            CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevent_self_follow',
            )
        ]
