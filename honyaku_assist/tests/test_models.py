from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from ..models import Engine

from freezegun import freeze_time


class EngineModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.engine = Engine.objects.create(name="Google")

    # Check field labels are correct when object created

    def test_name_label(self):
        field_label = self.engine._meta.get_field("name").verbose_name

        self.assertEqual(field_label, "name")
        self.assertNotEqual(field_label, "")

    def test_current_usage_label(self):
        field_label = self.engine._meta.get_field("current_usage").verbose_name

        self.assertEqual(field_label, "current usage")
        self.assertNotEqual(field_label, "current_usage")
        self.assertNotEqual(field_label, "")

    def test_month_usage_last_reset_label(self):
        field_label = self.engine._meta.get_field("month_usage_last_reset").verbose_name

        self.assertEqual(field_label, "month usage last reset")
        self.assertNotEqual(field_label, "month_usage_last_reset")
        self.assertNotEqual(field_label, "")

    def test_year_usage_last_reset_label(self):
        field_label = self.engine._meta.get_field("year_usage_last_reset").verbose_name

        self.assertEqual(field_label, "year usage last reset")
        self.assertNotEqual(field_label, "year_usage_last_reset")
        self.assertNotEqual(field_label, "")

    # Check field values are correct when object created

    def test_name_field_when_created(self):
        self.assertEqual(self.engine.name, "Google")
        self.assertNotEqual(self.engine.name, "")
        self.assertNotEqual(self.engine.name, None)

    def test_current_usage_field_when_created(self):
        self.assertEqual(self.engine.current_usage, 0)
        self.assertNotEqual(self.engine.current_usage, None)

    def test_month_usage_last_reset_field_when_created(self):
        current_month = timezone.now().month

        self.assertEqual(self.engine.month_usage_last_reset, current_month)
        self.assertNotEqual(self.engine.month_usage_last_reset, 0)
        self.assertNotEqual(self.engine.month_usage_last_reset, None)

    def test_year_usage_last_reset_field_when_created(self):
        current_year = timezone.now().year

        self.assertEqual(self.engine.year_usage_last_reset, current_year)
        self.assertNotEqual(self.engine.year_usage_last_reset, 0)
        self.assertNotEqual(self.engine.year_usage_last_reset, None)

    # Check field properties

    def test_name_max_length(self):
        max_length = self.engine._meta.get_field("name").max_length

        self.assertEqual(max_length, 100)

    def test_current_usage_default_value(self):
        default = self.engine._meta.get_field("current_usage").default

        self.assertEqual(default, 0)

    def test_month_usage_last_reset_default_value(self):
        default = self.engine._meta.get_field("month_usage_last_reset").default

        self.assertEqual(default, timezone.now().month)

    def test_year_usage_last_reset_default_value(self):
        default = self.engine._meta.get_field("year_usage_last_reset").default

        self.assertEqual(default, timezone.now().year)

    # Check meta fields

    def test_verbose_name(self):
        verbose_name = self.engine._meta.verbose_name

        self.assertEqual(verbose_name, "engine")
        self.assertNotEqual(verbose_name, "")
        self.assertNotEqual(verbose_name, None)

    def test_verbose_name_plural(self):
        verbose_name_plural = self.engine._meta.verbose_name_plural

        self.assertEqual(verbose_name_plural, "engines")
        self.assertNotEqual(verbose_name_plural, "engine")
        self.assertNotEqual(verbose_name_plural, "")
        self.assertNotEqual(verbose_name_plural, None)

    # Check class methods

    def test_str_representation_method(self):
        self.assertEqual(str(self.engine), "Google")
        self.assertNotEqual(str(self.engine), "")
        self.assertNotEqual(str(self.engine), None)

    @freeze_time("2023-01-01")
    def test_update_usage_method_when_reset_previous_month(self):
        """
        Test that usage is reset to the length of source text if the usage
        hasn't been reset in the current month.
        """

        # Create an engine that was last updated the previous month.
        deepl_engine = Engine.objects.create(
            name="DeepL",
            current_usage=500,
            month_usage_last_reset=12,
            year_usage_last_reset=2022,
        )

        # Check that object has been created properly.
        self.assertEqual(deepl_engine.name, "DeepL")
        self.assertEqual(deepl_engine.current_usage, 500)
        self.assertEqual(deepl_engine.month_usage_last_reset, 12)
        self.assertEqual(deepl_engine.year_usage_last_reset, 2022)
        self.assertNotEqual(deepl_engine.name, "")
        self.assertNotEqual(deepl_engine.current_usage, 0)
        self.assertNotEqual(deepl_engine.month_usage_last_reset, 1)
        self.assertNotEqual(deepl_engine.year_usage_last_reset, 2023)

        # Update the usage.
        source_text = "これはテストです。"
        deepl_engine.update_usage(source_text)

        # Check that the usage has been reset to the length of the current
        # source text of 9 rather than the length of the source text being added
        # to the previous month's value of 500 to make 509.
        self.assertEqual(deepl_engine.current_usage, 9)
        self.assertNotEqual(deepl_engine.current_usage, 509)

        # Check that the month and year values have also been updated.
        self.assertEqual(deepl_engine.month_usage_last_reset, 1)
        self.assertEqual(deepl_engine.year_usage_last_reset, 2023)
        self.assertNotEqual(deepl_engine.month_usage_last_reset, 12)
        self.assertNotEqual(deepl_engine.year_usage_last_reset, 2022)

    @freeze_time("2023-01-01")
    def test_update_usage_method_when_already_reset_current_month(self):
        """
        Test that the source text length is added to the current usage value
        if the usage has been reset in the current month.
        """

        # Create an engine that was last updated in the current month.
        cotoha_engine = Engine.objects.create(
            name="Cotoha",
            current_usage=500,
            month_usage_last_reset=1,
            year_usage_last_reset=2023,
        )

        # Check that object has been created properly.
        self.assertEqual(cotoha_engine.name, "Cotoha")
        self.assertEqual(cotoha_engine.current_usage, 500)
        self.assertEqual(cotoha_engine.month_usage_last_reset, 1)
        self.assertEqual(cotoha_engine.year_usage_last_reset, 2023)
        self.assertNotEqual(cotoha_engine.name, "")
        self.assertNotEqual(cotoha_engine.current_usage, 0)
        self.assertNotEqual(cotoha_engine.month_usage_last_reset, 2022)
        self.assertNotEqual(cotoha_engine.year_usage_last_reset, 12)

        # Update the usage.
        source_text = "これはテストです。"
        cotoha_engine.update_usage(source_text)

        # The length of the source text should have bern added to the previous
        # month's value of 500 to make 509.
        self.assertEqual(cotoha_engine.current_usage, 509)
        self.assertNotEqual(cotoha_engine.current_usage, 9)

        # Check that the month and year values have not been changed.
        self.assertEqual(cotoha_engine.month_usage_last_reset, 1)
        self.assertEqual(cotoha_engine.year_usage_last_reset, 2023)
