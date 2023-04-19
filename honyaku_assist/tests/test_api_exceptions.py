from unittest.mock import patch

from django.urls import reverse
from django.test import TestCase

from ..models import Engine


class TestHandlingOfExceptionsFromDeepL(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.engine = Engine.objects.create(name="Google")

    def test_deepl_api_exception_bad_language_codes(self):
        with patch("honyaku_assist.views.get_source_target_languages") as mocked_func:
            mocked_func.return_value = "xx", "xx"
            self.response = self.client.post(
                reverse("index"),
                {"translation_direction": "Ja>En", "source_text": "花粉飛散情報"},
            )

            mocked_func.assert_called_once()
            self.assertContains(self.response, "DeepL error")
            self.assertContains(self.response, "Google error")
