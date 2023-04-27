from unittest.mock import patch

from django.urls import reverse
from django.test import TestCase


class TestTranslateView(TestCase):
    
    def setUp(self):

        # Mock calls to the DeepL and Google APIs.
        with patch("honyaku_assist.views.call_deepl_api") as mock_deepl_call, \
             patch("honyaku_assist.views.call_google_api_v3") as mock_google_call:

            # Mock the values returned by call_deepl_api() in the view.
            deepl_result, deepl_usage = "Pollen dispersal information", 50
            mock_deepl_call.return_value = deepl_result, deepl_usage

            # Mock the values returned by call_google_api_v3() in the view.
            google_result, google_usage = "Pollen dispersion information", 70
            mock_google_call.return_value = google_result, google_usage

            # Make a request to the view.
            self.response = self.client.post(
                reverse("index"),
                {"translation_direction": "Ja>En", "source_text": "花粉飛散情報"},
            )

            # Assert that mocked functions are actually called.
            mock_deepl_call.assert_called_once()
            mock_google_call.assert_called_once()

    def test_output_page_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_output_page_context_contains_submitted_data(self):
        self.assertEqual(self.response.context["source_lang"], "ja")
        self.assertEqual(self.response.context["target_lang"], "en-us")
        self.assertEqual(self.response.context["source_text"], "花粉飛散情報")
        self.assertEqual(self.response.context["source_text_length"], 6)

    def test_output_page_context_deepl_data(self):
        self.assertEqual(self.response.context["deepl_result"], "Pollen dispersal information")
        self.assertEqual(self.response.context["deepl_result_length"], 28)
        self.assertEqual(self.response.context["deepl_usage"], 50)

    def test_output_page_context_google_data(self):
        self.assertEqual(self.response.context["google_result"], "Pollen dispersion information")
        self.assertEqual(self.response.context["google_result_length"], 29)
        self.assertEqual(self.response.context["google_usage"], 70)

    def test_output_page_templates_used(self):
        self.assertTemplateUsed(self.response, "results.html")

    def test_output_page_content(self):
        self.assertContains(self.response, "DeepL result")
        self.assertContains(self.response, "Pollen dispersal information")
        self.assertContains(self.response, "Google result")
        self.assertContains(self.response, "Pollen dispersion information")
