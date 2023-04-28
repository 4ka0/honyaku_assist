from django.db import models
from django.utils import timezone


class Engine(models.Model):
    """
    Model for a machine translation engine.
    Created essentially to store usage values for engines that don't provide a
    way to get the usage via their API.
    """

    name = models.CharField(max_length=100)
    current_usage = models.IntegerField(default=0)

    # The month/year the usage was last reset
    month_usage_last_reset = models.IntegerField(default=timezone.now().month)
    year_usage_last_reset = models.IntegerField(default=timezone.now().year)

    class Meta:
        verbose_name = "engine"
        verbose_name_plural = "engines"
        app_label = "honyaku_assist"

    def __str__(self):
        return self.name

    def update_usage(self, source_text):
        """
        Method to update the usage of the engine.
        Takes into account the fact that the usage needs to be reset each month.

        Args:
            self (Engine obj): An instance of the engine in question.
            source_text (str): The source text to be translated.

        """

        current_month: tuple = (timezone.now().month, timezone.now().year)
        month_last_reset: tuple = (self.month_usage_last_reset, self.year_usage_last_reset)

        if month_last_reset != current_month:
            # Reset usage value (to the length of the source text to be translated).
            self.current_usage = len(source_text)
            # Update the usage reset date values.
            self.month_usage_last_reset = current_month[0]
            self.year_usage_last_reset = current_month[1]
        else:
            self.current_usage += len(source_text)

        self.save()
