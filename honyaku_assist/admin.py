from django.contrib import admin

from .models import Engine


class EngineAdmin(admin.ModelAdmin):
    fields = ("name", "current_usage")
    list_display = ("name", "current_usage", "month_usage_last_reset")


admin.site.register(Engine, EngineAdmin)
