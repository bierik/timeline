from django.contrib import admin

from timeline.image.models import Image
from timeline.people import models


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    search_fields = ["name"]
    list_display_links = ["name"]
    inlines = [ImageInline]
    filter_horizonal = ("relations",)
