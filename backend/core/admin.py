from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.authentication.models import User
from core.events.models import Event
from core.image.models import Image
from core.people.models import Person
from core.role.models import Role


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    search_fields = ["name"]
    list_display_links = ["name"]
    inlines = [ImageInline]
    filter_horizonal = ("relations",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["pk", "title"]
    search_fields = ["title"]
    list_display_links = ["title"]
    inlines = [ImageInline]
    filter_horizonal = ("relations",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
