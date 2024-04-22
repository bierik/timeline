import io
import os
from pathlib import Path

import pyvips
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from core.image.models import Image


class Event(TimeStampedModel):
    title = models.CharField(verbose_name=_("Titel"), max_length=255)
    date = models.DateField(verbose_name=_("Datum"))
    description = models.TextField(verbose_name=_("Beschreibung"), null=True, blank=True)
    icon = models.CharField(verbose_name=_("Icon"), max_length=255, blank=True)
    relations = models.ManyToManyField(
        "Event",
        verbose_name=_("Relationen"),
        blank=True,
        related_name="reverse_relations",
    )

    class Meta:
        ordering = ["created", "title"]
        verbose_name = _("Ereignis")
        verbose_name_plural = _("Ereignisse")

    def __str__(self):
        return self.title

    def add_image(self, name):
        image_path = Path(settings.TUS_DESTINATION_DIR) / name
        with pyvips.Image.new_from_file(image_path) as image:
            image = image.autorot()
            event_image = Image.objects.create(title="title", event=self, width=image.width, height=image.height)
            event_image.file.save(
                name,
                io.BytesIO(image.write_to_buffer(".jpeg", **{"Q": 80, "strip": True})),
            )
            os.remove(image_path)
