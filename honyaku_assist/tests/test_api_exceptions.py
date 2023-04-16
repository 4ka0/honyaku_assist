from django.test import TestCase
from django.urls import reverse

from ..models import Engine


class TestHandlingOfExceptionsFromDeepL(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.engine = Engine.objects.create(name="Google")

    def test_deepl_api_exception_handling_1(self):

        # Use the below
        # Intentionally cause exceptions from deepl
        # Check the error message displayed on the page
        # Check what exceptions can be received from DeepL, try and cause one

        response = self.client.post(
            reverse('index'),
            {'translation_direction': 'Ja>En', 'source_text': '花粉飛散情報'}
        )

        # print(response.content)
        # print(response.context)
