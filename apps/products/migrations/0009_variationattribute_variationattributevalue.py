# Generated by Django 5.1.6 on 2025-02-22 18:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0008_productseo"),
    ]

    operations = [
        migrations.CreateModel(
            name="VariationAttribute",
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
                ("attribute_name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "active_status",
                    models.CharField(
                        blank=True,
                        choices=[("active", "Active"), ("inactive", "Inactive")],
                        default="active",
                        max_length=10,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Variation Attribute",
                "verbose_name_plural": "Variation Attribute",
                "db_table": "variation_attribute",
                "ordering": ["-id"],
                "indexes": [
                    models.Index(fields=["id"], name="variation_a_id_7031d0_idx"),
                    models.Index(
                        fields=["attribute_name"], name="variation_a_attribu_20c83e_idx"
                    ),
                    models.Index(
                        fields=["active_status"], name="variation_a_active__62449b_idx"
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="VariationAttributeValue",
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
                ("attribute_value", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "active_status",
                    models.CharField(
                        blank=True,
                        choices=[("active", "Active"), ("inactive", "Inactive")],
                        default="active",
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "variation_attribute",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variation_attribute_value",
                        to="products.variationattribute",
                    ),
                ),
            ],
            options={
                "verbose_name": "Variation Attribute Value",
                "verbose_name_plural": "Variation Attribute Values",
                "db_table": "variation_attribute_value",
                "ordering": ["-id"],
                "indexes": [
                    models.Index(fields=["id"], name="variation_a_id_cbaa77_idx"),
                    models.Index(
                        fields=["attribute_value"],
                        name="variation_a_attribu_0142f1_idx",
                    ),
                    models.Index(
                        fields=["active_status"], name="variation_a_active__25e4e7_idx"
                    ),
                ],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("variation_attribute", "attribute_value"),
                        name="unique_attribute_value",
                    )
                ],
            },
        ),
    ]
