# Generated by Django 4.2.2 on 2023-10-30 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0005_alter_post_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post", name="title", field=models.CharField(max_length=200),
        ),
    ]
