from django.contrib import admin

from django.contrib import admin

from timeline.events import models


class ImageInline(admin.TabularInline):
    model = models.Image

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["pk", "title"]
    search_fields = ["title"]
    list_display_links = ["title"]
    inlines = [ImageInline]

@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["pk", "title"]
    search_fields = ["title"]
    list_display_links = ["title"]
