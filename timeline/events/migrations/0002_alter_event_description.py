# Generated by Django 3.2.8 on 2022-02-06 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="description",
            field=models.JSONField(null=True, verbose_name="Beschreibung"),
        ),
    ]
