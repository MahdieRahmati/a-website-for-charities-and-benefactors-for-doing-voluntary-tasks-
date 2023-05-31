# Generated by Django 4.2 on 2023-05-22 15:58

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="address",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="gender",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female"), ("MF", "Unset")],
                default="MF",
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(
                blank=True,
                max_length=15,
                validators=[accounts.validators.PhoneValidator()],
            ),
        ),
    ]
