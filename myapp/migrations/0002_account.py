# Generated by Django 4.2.2 on 2023-10-30 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
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
                ("userid", models.CharField(max_length=20)),
                ("name", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=20)),
            ],
        ),
    ]
