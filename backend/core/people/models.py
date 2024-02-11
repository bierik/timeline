from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Person(TimeStampedModel):
    class Roles(models.IntegerChoices):
        GODFATHER = 1, _("Gotte/Götti")

    name = models.CharField(verbose_name=_("Name"), max_length=255)
    role = models.IntegerField(verbose_name=_("Rolle"), choices=Roles.choices)
    events = models.ManyToManyField("Event", verbose_name=_("Ereignis"), related_name="people", blank=True)

    class Meta:
        ordering = ["created"]
        verbose_name = _("Person")
        verbose_name_plural = _("Personen")
