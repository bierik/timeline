from django.contrib import admin

from timeline.events import models
from timeline.image.models import Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["pk", "title"]
    search_fields = ["title"]
    list_display_links = ["title"]
    inlines = [ImageInline]
    filter_horizonal = ("relations",)
