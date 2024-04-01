from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Event(TimeStampedModel):
    title = models.CharField(verbose_name=_("Titel"), max_length=255)
    date = models.DateField(verbose_name=_("Datum"))
    description = models.TextField(verbose_name=_("Beschreibung"), null=True)
    icon = models.CharField(verbose_name=_("Icon"), max_length=255, blank=True)
    relations = models.ManyToManyField(
        "Event",
        verbose_name=_("Relationen"),
        blank=True,
        related_name="reverse_relations",
    )

    class Meta:
        ordering = ["created"]
        verbose_name = _("Ereignis")
        verbose_name_plural = _("Ereignisse")

    def __str__(self):
        return self.title
