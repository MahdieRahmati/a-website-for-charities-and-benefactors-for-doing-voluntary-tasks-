# Generated by Django 4.1.7 on 2023-04-06 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("charities", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="task",
            old_name="assigned_benifactor",
            new_name="assigned_benefactor",
        ),
    ]