from django.db import models
from django.utils import timezone


class Engine(models.Model):
    """ Model for a machine translation engine.
        Used to store the current usage for the engine in question. """

    name = models.CharField(max_length=100)
    current_usage = models.IntegerField(default=0)
    usage_last_reset_month = models.IntegerField(default=timezone.now().month)
    usage_last_reset_year = models.IntegerField(default=timezone.now().year)

    class Meta:
        verbose_name = "engine"
        verbose_name_plural = "engines"

    def __str__(self):
        return self.name

    def get_current_usage(self):
        return self.current_usage

    def update_usage(self, translated_text):

        # Create a tuple holding the current month and year such as '(4, 2023)'.
        current_month_year = (timezone.now().month, timezone.now().year)

        # Create similar tuple for month/year the usage was last reset.
        usage_last_reset_month_year = (self.usage_last_reset_month, self.usage_last_reset_year)

        # Reset the usage if not already been reset this month.
        # Otherwise, add the length of the translated text to the current usage.
        if usage_last_reset_month_year != current_month_year:
            self.usage_last_reset_month = current_month_year[0]
            self.usage_last_reset_year = current_month_year[1]
            self.current_usage = len(translated_text)
        else:
            self.current_usage += len(translated_text)
