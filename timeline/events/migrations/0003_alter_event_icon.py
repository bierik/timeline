# Generated by Django 3.2.8 on 2022-01-02 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='icon',
            field=models.CharField(blank=True, max_length=2, verbose_name='Icon'),
        ),
    ]