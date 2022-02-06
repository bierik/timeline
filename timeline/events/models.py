from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Event(TimeStampedModel):
    title = models.CharField(verbose_name=_("Titel"), max_length=255)
    date = models.DateField(verbose_name=_("Datum"))
    description = models.TextField(verbose_name=_("Beschreibung"), blank=True)
    icon = models.CharField(verbose_name=_("Icon"), max_length=255, blank=True)

    class Meta:
        ordering = ["created"]
        verbose_name = _("Ereignis")
        verbose_name_plural = _("Ereignisse")


class Media(TimeStampedModel):
    title = models.CharField(verbose_name=_("Titel"), max_length=255)
    description = models.TextField(verbose_name=_("Beschreibung"), blank=True)

    class Meta:
        abstract = True

class Image(Media):
    event = models.ForeignKey(Event, verbose_name=_("Ereignis"), related_name=_("images"), on_delete=models.PROTECT)
    file = models.ImageField(verbose_name=_("Bilddatei"))

    class Meta:
        ordering = ["created"]
        verbose_name = _("Bild")
        verbose_name_plural = _("Bilder")
