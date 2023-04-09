from django.db import models
from django.utils import timezone


class Engine(models.Model):
    """ Model for a machine translation engine.
        Created essentially to store usage values for engines that don't provide
        a way to get the usage via their API. """

    name = models.CharField(max_length=100)
    current_usage = models.IntegerField(default=0)

    # The month/year the usage was last reset
    usage_last_reset_month = models.IntegerField(default=timezone.now().month)
    usage_last_reset_year = models.IntegerField(default=timezone.now().year)

    class Meta:
        verbose_name = "engine"
        verbose_name_plural = "engines"

    def __str__(self):
        return self.name
