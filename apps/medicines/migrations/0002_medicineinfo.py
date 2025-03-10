# Generated by Django 5.1.6 on 2025-02-24 19:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medicines", "0001_initial"),
        ("products", "0010_productvariation"),
    ]

    operations = [
        migrations.CreateModel(
            name="MedicineInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_required_prescription", models.BooleanField(default=True)),
                ("pharmacology", models.TextField(blank=True, null=True)),
                ("indication", models.TextField(blank=True, null=True)),
                ("composition", models.TextField(blank=True, null=True)),
                ("dosage_details", models.TextField(blank=True, null=True)),
                ("administration", models.TextField(blank=True, null=True)),
                ("interaction", models.TextField(blank=True, null=True)),
                ("contraindication", models.TextField(blank=True, null=True)),
                ("side_effect", models.TextField(blank=True, null=True)),
                ("pregnancy_and_lactation", models.TextField(blank=True, null=True)),
                ("precautions_and_warning", models.TextField(blank=True, null=True)),
                ("use_special_population", models.TextField(blank=True, null=True)),
                ("overdose_effects", models.TextField(blank=True, null=True)),
                ("therapeutic_class", models.TextField(blank=True, null=True)),
                ("treatment_duration", models.TextField(blank=True, null=True)),
                ("reconstitution", models.TextField(blank=True, null=True)),
                ("storage_condition", models.TextField(blank=True, null=True)),
                ("chemical_structure", models.TextField(blank=True, null=True)),
                (
                    "chemical_structure_image",
                    models.ImageField(blank=True, null=True, upload_to="medicine/"),
                ),
                (
                    "active_status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "Inactive")],
                        default="active",
                        max_length=10,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "generic_name",
                    models.ManyToManyField(
                        blank=True,
                        related_name="medicine_generic_name",
                        to="medicines.genericnameinformation",
                    ),
                ),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="medicine_info",
                        to="products.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Medicine Info",
                "verbose_name_plural": "Medicine Info",
                "db_table": "medicine_info",
                "ordering": ["-id"],
                "indexes": [
                    models.Index(fields=["id"], name="medicine_in_id_0c0f99_idx"),
                    models.Index(
                        fields=["product"], name="medicine_in_product_c87874_idx"
                    ),
                    models.Index(
                        fields=["active_status"], name="medicine_in_active__7721d4_idx"
                    ),
                    models.Index(
                        fields=["is_required_prescription"],
                        name="medicine_in_is_requ_034794_idx",
                    ),
                ],
            },
        ),
    ]
