from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from commons.models import SoftDeleteBaseModel, TimeAndUUIDStampedBaseModel

from .enums import UserPrefix
from .managers import UserManager


class User(SoftDeleteBaseModel, AbstractUser, TimeAndUUIDStampedBaseModel):
    username = models.CharField(
        _("username"),
        max_length=20,
        unique=True,
        null=True,
        blank=False,
        db_index=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("That username is not available"),
        },
    )

    email = models.EmailField(
        _("email address"),
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
        error_messages={
            "unique": _("That email is not available"),
        },
    )
    first_name = models.CharField(
        _("first name"), max_length=100, null=False, blank=False
    )
    last_name = models.CharField(
        _("last name"), max_length=100, null=False, blank=False
    )
    prefix = models.CharField(
        _("prefix"), max_length=20, choices=UserPrefix.choices, null=True, blank=True
    )
    phone_regex = RegexValidator(
        regex=r"^\+\d{8,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=16, null=True, blank=True
    )
    job_title = models.CharField(_("job_title"), max_length=100, null=True, blank=True)
    company = models.CharField(_("company"), max_length=100, null=True, blank=True)
    website = models.URLField(_("website"), max_length=100, null=True, blank=True)
    blog = models.URLField(_("blog"), max_length=100, null=True, blank=True)
    country = CountryField(_("country"), null=True, blank=True, default="GB")
    postal_code = models.IntegerField(_("postal_code"), null=True, blank=True)
    is_email_verified = models.BooleanField(_("is_email_verified"), default=False)
    email_verified_at = models.DateTimeField(
        _("email_verified_at"), blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        "username",
        "first_name",
        "last_name",
    )

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def get_absolute_url(self):
        return reverse("accounts:user", args=[str(self.id)])

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def profile_url(self) -> str:
        hex_name = self.get_full_name().encode().hex()
        return f"https://avatars.dicebear.com/api/bottts/{hex_name}.svg/size=16"
