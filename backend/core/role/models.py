from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=255)

    def __str__(self):
        return self.name
