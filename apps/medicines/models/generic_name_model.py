from django.core.exceptions import ValidationError

# Django Model Fields
from django.db.models import (
    CharField,
    ImageField,
    Index,
    TextField,
)
from django.utils.translation import gettext_lazy as _

from apps.common.models import (
    ActiveStatusChoices,
    DjangoBaseModel,
)


# * <<-------------------------------------*** GENERIC NAME INFORMATION TABLE ***-------------------------------->>
class GenericNameInformation(DjangoBaseModel):
    """
    *Generic Name Information database Table
    """

    generic_name = CharField(max_length=250, unique=True)
    drug_category = CharField(max_length=150, blank=True, null=True)
    chemical_name = CharField(max_length=250, blank=True, null=True)
    chemical_formula = CharField(max_length=250, blank=True, null=True)
    formula_image = ImageField(upload_to="generic_name/", blank=True, null=True)
    active_ingredients = CharField(max_length=250, blank=True, null=True)
    brand_equivalents = CharField(max_length=250, blank=True, null=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices,
        default=ActiveStatusChoices.ACTIVE,
    )
    description = TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Generic Name Information")
        verbose_name_plural = _("Generic Name Information")
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["generic_name"]),
            Index(fields=["active_status"]),
        ]
        app_label = "medicines"
        db_table = "generic_name_information"

    def clean(self):
        """
        Custom validation to ensure generic_name is unique.
        Raises a ValidationError if a generic with the same name already exists.
        """
        if self.__class__.objects.filter(generic_name=self.generic_name).exists():
            raise ValidationError(
                _("A generic with this name already exists."),
            )

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.generic_name}"

    def __repr__(self):
        return f"<GenericNameInformation: {self.generic_name}>"
