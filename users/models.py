from decouple import config
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from common.models import TimeStampedModel
import uuid


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    model for user informations
    """
    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    firebase_uuid = models.CharField(max_length=200, blank=True, default='',
                                     help_text="Firebase uuid of user")
    profile_picture = models.URLField(
        help_text="Photo of user",
        default=None,
        null=True,
        blank=True
    )
    push_notification = models.BooleanField(
        default=True,
        help_text="Does the user wants push notifications from Nebuyo?"
    )
    newsletter_notification = models.BooleanField(
        _('newsletter notification'),
        default=True,
        help_text=_("Does the user wants newsletter subscriptions?")
    )
    gender = models.CharField(max_length=30, default='', blank=True, null=True,
                              help_text="Gender of user")
    
    reward_points = models.PositiveIntegerField(
        _('reward points'),
        default=0,
        help_text=_(
            'points received after purchasing product.'
        )
    )
    
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('user')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.email


class FacebookDataDelete(TimeStampedModel):
    STATUS = (
        ('completed', 'completed'),
        ('initiated', 'initiated')
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('users.User', default=None, blank=True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS)

    def __str__(self):
        return f'{self.user.email} status: {self.status}'


class Shipping(TimeStampedModel):
    """
    Model to store user's shipping information.
    """
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='shippings',
    )
    area = models.ForeignKey(
        'core.Area',
        on_delete=models.CASCADE,
        related_name='area_shippings',
    )
    street_address = models.CharField(max_length=512, default="")
    postal_code = models.CharField(max_length=255, default="")
    first_name = models.CharField(max_length=64, blank=True, default="")
    last_name = models.CharField(max_length=64, blank=True, default="")
    email = models.EmailField(_('email address'))
    phone_no = models.CharField(max_length=50, default="", blank=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Shipping')
        verbose_name_plural = _('Shipping')
        ordering = ('-created_on',)
    
    def __str__(self):
        return f'{self.street_address}'

