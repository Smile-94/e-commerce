# Generated by Django 5.1.6 on 2025-02-21 09:04

import django.contrib.auth.models
import django.contrib.auth.validators
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
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
                    "name",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Name"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=50,
                        null=True,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="Username",
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="password"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        null=True,
                        unique=True,
                        verbose_name="Email",
                    ),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        max_length=128,
                        null=True,
                        region=None,
                        unique=True,
                        verbose_name="Contact Number",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        blank=True,
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        null=True,
                        verbose_name="Is Active",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        blank=True, default=False, null=True, verbose_name="Is Staff"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "user",
                "db_table": "user",
                "ordering": ["-id"],
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
