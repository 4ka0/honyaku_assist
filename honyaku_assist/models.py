from django.db import models


class Engine(models.Model):
    name = models.CharField(max_length=100)
    current_usage = models.IntegerField(default=0)
    month_usage_last_reset = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "engine"
        verbose_name_plural = "engines"

    def __str__(self):
        return self.name
