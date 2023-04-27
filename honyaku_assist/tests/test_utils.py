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
        Engine.objects.create(name="Google")
        source_text = "これはテストです。"
        source_text_len = len(source_text)
        usage = get_google_usage(source_text)

        self.assertEqual(usage, source_text_len)
        self.assertNotEqual(usage, 0)
