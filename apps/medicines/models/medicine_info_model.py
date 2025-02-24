from common.models import ActiveStatusChoices, DjangoBaseModel

# Django Model Fields
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    ForeignKey,
    ImageField,
    Index,
    OneToOneField,
    TextField,
)
from django.utils.translation import gettext_lazy as _

from apps.medicines.models.generic_name_model import GenericNameInformation

# Import other models
from apps.products.models.product_model import Product


# * <<-------------------------------*** MEDICINE INFO TABLE ***--------------------------------->>
class MedicineInfo(DjangoBaseModel):
    """
    *Medicine Info database Table
    """

    product = OneToOneField(Product, related_name="medicine_info", on_delete=CASCADE)
    generic_name = ForeignKey(
        GenericNameInformation,
        related_name="medicine_generic_name",
        on_delete=SET_NULL,
        blank=True,
        null=True,
    )
    is_required_prescription = BooleanField(default=True)
    pharmacology = TextField(blank=True, null=True)
    indication = TextField(blank=True, null=True)
    composition = TextField(blank=True, null=True)
    dosage_details = TextField(blank=True, null=True)
    administration = TextField(blank=True, null=True)
    interaction = TextField(blank=True, null=True)
    contraindication = TextField(blank=True, null=True)
    side_effect = TextField(blank=True, null=True)
    pregnancy_and_lactation = TextField(blank=True, null=True)
    precautions_and_warning = TextField(blank=True, null=True)
    use_special_population = TextField(blank=True, null=True)
    overdose_effects = TextField(blank=True, null=True)
    therapeutic_class = TextField(blank=True, null=True)
    treatment_duration = TextField(blank=True, null=True)
    reconstitution = TextField(blank=True, null=True)
    storage_condition = TextField(blank=True, null=True)
    chemical_structure = TextField(blank=True, null=True)
    chemical_structure_image = ImageField(upload_to="medicine/", blank=True, null=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices,
        default=ActiveStatusChoices.ACTIVE,
    )
    description = TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Medicine Info")
        verbose_name_plural = _("Medicine Info")
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["product"]),
            Index(fields=["active_status"]),
            Index(fields=["is_required_prescription"]),
        ]
        app_label = "medicines"
        db_table = "medicine_info"

    def __str__(self):
        return f"{self.product.name}"

    def __repr__(self):
        return f"<MedicineInfo: {self.product.name}>"
