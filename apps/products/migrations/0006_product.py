# Generated by Django 5.1.6 on 2025-02-22 06:30

import django.db.models.deletion
import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0005_vat"),
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("product_id", models.CharField(max_length=30, unique=True)),
                ("product_name", models.CharField(max_length=255)),
                (
                    "product_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("medicine", "Medicine"),
                            ("device", "Device"),
                            ("service", "Service"),
                            ("general", "General"),
                            ("book", "Book"),
                            ("other", "Other"),
                        ],
                        default="general",
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "product_image",
                    models.ImageField(blank=True, null=True, upload_to="product/"),
                ),
                ("image_alt_name", models.CharField(max_length=255)),
                (
                    "barcode_type",
                    models.CharField(
                        blank=True,
                        choices=[("manual", "Manual"), ("auto", "Auto")],
                        default="manual",
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "barcode",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("url_slug", models.CharField(blank=True, max_length=255, null=True)),
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
                    "brand",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_brand",
                        to="products.brand",
                    ),
                ),
                (
                    "manufacturer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="products.manufacturer",
                    ),
                ),
                (
                    "product_unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_unit",
                        to="products.unitattributevalue",
                    ),
                ),
                (
                    "purchase_vat",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="purchase_vat_amount",
                        to="products.vat",
                    ),
                ),
                (
                    "sales_vat",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sales_vat_amount",
                        to="products.vat",
                    ),
                ),
                (
                    "search_keyword",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="search_keyword",
                    ),
                ),
                (
                    "sub_category",
                    models.ManyToManyField(
                        blank=True,
                        related_name="product_sub_category",
                        to="products.subcategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Product",
                "db_table": "product",
                "ordering": ["-id"],
                "indexes": [
                    models.Index(fields=["id"], name="product_id_a3d46d_idx"),
                    models.Index(
                        fields=["product_id"], name="product_product_a470af_idx"
                    ),
                    models.Index(
                        fields=["product_type"], name="product_product_f634b9_idx"
                    ),
                    models.Index(fields=["barcode"], name="product_barcode_d2887e_idx"),
                    models.Index(fields=["brand"], name="product_brand_i_080bb1_idx"),
                    models.Index(
                        fields=["manufacturer"], name="product_manufac_766aee_idx"
                    ),
                    models.Index(
                        fields=["active_status"], name="product_active__f101c0_idx"
                    ),
                ],
            },
        ),
    ]
