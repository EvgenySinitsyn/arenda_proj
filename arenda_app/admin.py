from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Space, SpaceType, RentType, City, Building, SpaceImage


class SpaceImageAdmin(admin.StackedInline):
    model = SpaceImage


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    inlines = [SpaceImageAdmin]

    class Meta:
        model = Space


@admin.register(SpaceImage)
class SpacePhotoAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(SpaceType)
admin.site.register(RentType)
admin.site.register(City)
admin.site.register(Building)
