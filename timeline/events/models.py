from django.db import models
from django.utils.translation import gettext_lazy as _

class Event(models.Model):
    title = models.CharField(verbose_name=_("Titel"), max_length=255)
    date = models.DateField(verbose_name=_("Datum"))
    description = models.TextField(verbose_name=_("Beschreibung"), blank=True)
    icon = models.CharField(verbose_name=_("Icon"), max_length=255, blank=True)
