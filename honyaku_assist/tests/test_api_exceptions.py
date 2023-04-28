from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from ..models import Engine


class TestDisplayOfExceptionsFromAPIs(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.engine = Engine.objects.create(name="Google")

    def test_deepl_api_exception_bad_language_codes(self):
        """
        Uses bad language codes so that the DeepL and Google translation APIs
        return exceptions, then checks that the corresponding error strings
        appear in the response.
        """

        with patch("honyaku_assist.views.get_source_target_languages") as mocked_func:
            mocked_func.return_value = "xx", "xx"
            self.response = self.client.post(
                reverse("index"),
                {"translation_direction": "Ja>En", "source_text": "花粉飛散情報"},
            )

            mocked_func.assert_called_once()
            self.assertContains(self.response, "DeepL error")
            self.assertContains(self.response, "Google error")
