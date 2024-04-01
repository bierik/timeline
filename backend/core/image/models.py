from django.db import models
from django.utils.translation import gettext_lazy as _
from django_cleanup.signals import cleanup_pre_delete
from django_extensions.db.models import TimeStampedModel
from sorl.thumbnail import ImageField, delete


class Image(TimeStampedModel):
    title = models.CharField(verbose_name=_("Titel"), max_length=255)
    description = models.TextField(verbose_name=_("Beschreibung"), blank=True)

    person = models.OneToOneField(
        "Person",
        related_query_name="image",
        verbose_name=_("Ereignis"),
        on_delete=models.CASCADE,
        null=True,
    )
    event = models.ForeignKey(
        "Event",
        verbose_name=_("Ereignis"),
        related_name=_("images"),
        on_delete=models.CASCADE,
        null=True,
    )

    file = ImageField(verbose_name=_("Bilddatei"))
    width = models.PositiveIntegerField(blank=True, default=0)
    height = models.PositiveIntegerField(blank=True, default=0)

    class Meta:
        ordering = ["created"]
        verbose_name = _("Bild")
        verbose_name_plural = _("Bilder")


def cleanup_thumbnails(**kwargs):
    delete(kwargs["file"])


cleanup_pre_delete.connect(cleanup_thumbnails)
