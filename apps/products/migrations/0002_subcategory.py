# Generated by Django 5.1.6 on 2025-02-21 06:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubCategory",
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
                ("sub_category_name", models.CharField(max_length=255, unique=True)),
                ("parent_id", models.PositiveIntegerField(blank=True, default=0)),
                (
                    "sub_category_icon",
                    models.ImageField(
                        blank=True, null=True, upload_to="product/sub_categories"
                    ),
                ),
                ("is_client_usable", models.BooleanField(blank=True, default=False)),
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
                ("description", models.TextField(blank=True, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sub_category_category",
                        to="products.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sub-Category",
                "verbose_name_plural": "Sub-Category",
                "db_table": "sub_category",
                "ordering": ["-id"],
                "indexes": [
                    models.Index(fields=["id"], name="sub_categor_id_650cec_idx"),
                    models.Index(
                        fields=["sub_category_name"],
                        name="sub_categor_sub_cat_4dd523_idx",
                    ),
                    models.Index(
                        fields=["is_client_usable"],
                        name="sub_categor_is_clie_86acc2_idx",
                    ),
                    models.Index(
                        fields=["active_status"], name="sub_categor_active__f6abd7_idx"
                    ),
                ],
            },
        ),
    ]
