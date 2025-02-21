# from common.models import DjangoBaseModel, UserTypeChoice
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import DjangoBaseModel


class User(DjangoBaseModel, AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    """

    username_validator = UnicodeUsernameValidator()

    # User Information ######
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=50,
        null=True,
        blank=True,
    )

    username = models.CharField(
        verbose_name=_("Username"),
        max_length=50,
        unique=True,
        help_text=_(
            "Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.",
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=True,
        blank=True,
    )
    password = models.CharField(
        verbose_name=_("password"),
        max_length=200,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        unique=True,
        null=True,
        blank=True,
    )
    phone = PhoneNumberField(
        verbose_name=_("Contact Number"),
        unique=True,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Is Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
        ),
        null=True,
        blank=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_("Is Staff"),
        default=False,
        null=True,
        blank=True,
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "password", "phone"]
    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("user")
        ordering = ["-id"]
        db_table = "user"
        app_label = "user"

    @property
    def date_joined(self):
        return self.created_at

    def __str__(self):
        return str(self.username)
