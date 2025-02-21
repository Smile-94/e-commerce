from django.db.models import CharField, DateTimeField, Model, TextChoices


class ActiveStatusChoices(TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


class DjangoBaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
