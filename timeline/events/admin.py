from django.contrib import admin

from django.contrib import admin

from timeline.events import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["pk", "title"]
    search_fields = ["title"]
    list_display_links = ["title"]
