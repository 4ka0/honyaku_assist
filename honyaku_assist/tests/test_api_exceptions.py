from unittest.mock import patch

from django.urls import reverse
from django.test import TestCase

from ..models import Engine


class TestHandlingOfExceptionsFromDeepL(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.engine = Engine.objects.create(name="Google")

    def test_deepl_api_exception_bad_language_codes(self):

        # Use the below
        # Intentionally cause exceptions from deepl
        # Check the error message displayed on the page
        # Check what exceptions can be received from DeepL, try and cause one

        # response = self.client.post(
        #     reverse('index'),
        #     {'translation_direction': 'Ja>En', 'source_text': '花粉飛散情報'}
        # )

        # Mock call to get_source_target_languages(translation_direction) in utils.py
        with patch("honyaku_assist.views.get_source_target_languages") as mocked_func:

            # Mock the return values as erroneous language codes.
            mocked_func.return_value = "xx", "xx"

            # Make a request to the view.
            self.response = self.client.post(
                reverse("index"),
                {"translation_direction": "Ja>En", "source_text": "花粉飛散情報"},
            )

            # Assert that mocked functions are actually called.
            mocked_func.assert_called_once()

            print("++++++++++")
            print(self.response.content)
            print("++++++++++")
            print(self.response.context)
            print("++++++++++")
