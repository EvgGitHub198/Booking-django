# Generated by Django 4.2.2 on 2023-07-01 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
        ("booking", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.customuser"
            ),
        ),
    ]
