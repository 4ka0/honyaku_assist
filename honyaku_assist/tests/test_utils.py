from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from freezegun import freeze_time

from ..models import Engine
from ..utils import get_google_usage, get_source_target_languages


class TestGetSourceTargetLanguages(SimpleTestCase):
    def test_get_source_target_languages_Ja_to_En(self):
        translation_direction = "Ja>En"
        src_lang, tar_lang = get_source_target_languages(translation_direction)

        self.assertEqual(src_lang, "ja")
        self.assertEqual(tar_lang, "en-us")
        self.assertNotEqual(src_lang, "en-us")
        self.assertNotEqual(tar_lang, "ja")

    def test_get_source_target_languages_En_to_Ja(self):
        translation_direction = "En>Ja"
        src_lang, tar_lang = get_source_target_languages(translation_direction)

        self.assertEqual(src_lang, "en")
        self.assertEqual(tar_lang, "ja")
        self.assertNotEqual(src_lang, "ja")
        self.assertNotEqual(tar_lang, "en")


class TestGetGoogleUsage(TestCase):
    @freeze_time("2023-04-01")
    def test_get_google_usage(self):
        self.engine = Engine.objects.create(name="Google")
        self.source_text = "これはテストです。"
        self.source_text_len = len(self.source_text)
        usage = get_google_usage(self.source_text)

        self.assertEqual(usage, self.source_text_len)
        self.assertNotEqual(usage, 0)

    @freeze_time("2023-04-01")
    def test_engine_usage_is_reset(self):
        """Test that usage is reset to the length of source text
        if the usage hasn't been reset in the current month."""

        # Create engine that was last updated the previous month.
        self.engine = Engine.objects.create(
            name="Google",
            current_usage=500,
            month_usage_last_reset=3,
            year_usage_last_reset=2023,
        )
        self.source_text = "これはテストです。"
        usage = get_google_usage(self.source_text)

        # Usage should be reset to the length of the current source text (9)
        # rather than the length of the source text being added to the previous
        # month's value of 500 (509).
        self.assertEqual(usage, 9)
        self.assertNotEqual(usage, 509)

    @freeze_time("2023-04-01")
    def test_engine_usage_is_not_reset(self):
        """Test that the source text length is added to the current usage value
        if the usage has been reset in the current month."""

        # Create engine that was last updated in the current month.
        self.engine = Engine.objects.create(
            name="Google",
            current_usage=500,
            month_usage_last_reset=4,
            year_usage_last_reset=2023,
        )
        self.source_text = "これはテストです。"
        usage = get_google_usage(self.source_text)

        # The length of the source text should be added to the previous month's
        # value of 500 to make 509.
        self.assertEqual(usage, 509)
        self.assertNotEqual(usage, 9)
