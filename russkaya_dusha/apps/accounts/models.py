from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account_profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_("Аватар"))
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=_("Номер телефона должен быть в формате: '+999999999'. До 15 цифр.")
            )
        ],
        verbose_name=_("Номер телефона")
    )
    address = models.TextField(blank=True, null=True, verbose_name=_("Адрес"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Дата рождения"))
    passport_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Номер паспорта"))
    driver_license = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Номер водительского удостоверения"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата регистрации"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = _("Профиль пользователя")
        verbose_name_plural = _("Профили пользователей")
        ordering = ['-created_at']

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.account_profile.save()


# Create your models here.
