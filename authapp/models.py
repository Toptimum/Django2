from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)  # ImageField не будет работать без pillow
    age = models.PositiveIntegerField(verbose_name='Возраст пользователя', default=18)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    GENDER_CHOICES = (
        (None, 'Выберите пол'),
        (MALE, 'мужчина'),
        (FEMALE, 'женщина'),
    )
    # создание связи «один-к-одному» и создается индекс
    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='Теги', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name='О себе', max_length=512, blank=True)
    # получаем фиксированный набор значений, которые прописаны в кортеже GENDER_CHOICES
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDER_CHOICES, blank=True)

    class Meta:
        verbose_name_plural = 'Профили пользователей в соцсетях'
        verbose_name = 'Профиль пользователя'
        ordering = ['user']

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)  # при получении определенных сигналов вызывает задекорированный метод
    def save_user_profile(sender, instance, **kwargs):
        # из модели ShopUser можно получить доступ к связанной модели по ее имени как к атрибуту
        instance.shopuserprofile.save()
