# Generated by Django 3.2.8 on 2022-02-06 18:26

import django_editorjs_fields.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_alter_event_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="description",
            field=django_editorjs_fields.fields.EditorJsJSONField(
                null=True, verbose_name="Beschreibung"
            ),
        ),
    ]
