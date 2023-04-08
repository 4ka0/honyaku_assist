from django.contrib import admin

from .models import Engine


class EngineAdmin(admin.ModelAdmin):
    fields = ("name", "current_usage")
    list_display = (
        "name",
        "current_usage",
        "usage_last_reset_month",
        "usage_last_reset_year",
    )


admin.site.register(Engine, EngineAdmin)
