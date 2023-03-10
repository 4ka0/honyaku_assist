import requests
from unittest.mock import patch

from django.urls import reverse
from django.test import SimpleTestCase

from deepl import translator

from ..views import call_deepl_api


class TestHomepage(SimpleTestCase):

    def test_home_page_exists_at_desired_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_home_page_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'input.html')

    def test_home_page_title_and_navbar_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<title>Honyaku Assist</title>')

    def test_home_page_navbar_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<a class="navbar-brand" href="/">Honyaku Assist</a>')
        self.assertContains(
            response,
            '<span class="navbar-text">A machine translation assistant for'
        )

    def test_home_page_form_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Japanese to English')
        self.assertContains(response, 'English to Japanese')
        self.assertContains(
            response,
            '<button type="submit" class="btn btn-primary mt-2">Translate</button>'
        )


class TestOutput(SimpleTestCase):

    def setUp(self):

        # The below makes actual calls to the DeepL and Google APIs.
        """
        self.valid_data_response = self.client.post(
            reverse('home'),
            {'direction': 'Ja>En', 'source_text': '花粉飛散情報'}
        )
        """

        # The below mocks the calls to the DeepL and Google APIs.
        with patch('kikai_compare.views.call_deepl_api') as mock_deepl_call, \
            patch('kikai_compare.views.call_google_api_v3') as mock_google_call:

            # Mock the values returned by call_deepl_api() in the view.
            deepl_result, deepl_usage = 'Pollen dispersal information', 6
            mock_deepl_call.return_value = deepl_result, deepl_usage

            # Mock the values returned by call_google_api_v3() in the view.
            google_result = 'Pollen dispersion information'
            mock_google_call.return_value = google_result

            # Make a request to the view.
            self.response = self.client.post(
                reverse('home'),
                {'direction': 'Ja>En', 'source_text': '花粉飛散情報'}
            )

            # Assert that mocked functions are actually called.
            mock_deepl_call.assert_called_once()
            mock_google_call.assert_called_once()

    def test_output_page_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_output_page_context_contains_submitted_data(self):
        self.assertEqual(self.response.context['source_lang'], 'ja')
        self.assertEqual(self.response.context['target_lang'], 'en-us')
        self.assertEqual(self.response.context['source_text'], '花粉飛散情報')
        self.assertEqual(self.response.context['source_text_length'], 6)

    def test_output_page_context_deepl_data(self):
        self.assertEqual(self.response.context['deepl_result'], 'Pollen dispersal information')
        self.assertEqual(self.response.context['deepl_result_length'], 28)
        self.assertEqual(self.response.context['deepl_usage'], 6)

    def test_output_page_context_google_data(self):
        self.assertEqual(self.response.context['google_result'], 'Pollen dispersion information')
        self.assertEqual(self.response.context['google_result_length'], 29)

    """
    def test_output_page_with_valid_data_status_code(self):
        self.assertEqual(self.mocked_response.status_code, 200)

    def test_output_page_with_valid_data_templates_used(self):
        self.assertTemplateUsed(self.mocked_response, 'base.html')
        self.assertTemplateUsed(self.mocked_response, 'output.html')

    def test_output_page_with_valid_data_page_content(self):
        self.assertContains(self.mocked_response, 'Source text (JA)')
        self.assertContains(self.mocked_response, '(No. of characters: 6)')
        self.assertContains(self.mocked_response, 'DeepL result (EN-US)')
        self.assertContains(self.mocked_response, 'Google result (EN-US)')
        # Add tests to show mocked results from DeepL and Google are included in the output page
        # Tests are slow because each method is making real calls to the APIs

    def test_deep_api_exceptions(self):
        # Test exception is raised.
        # Test error message included in output.html.
        # Example, when en-us is set as the source language code:
        # (DeepL Error: Bad request, message: Value for 'source_lang' not supported.)
        pass
    """
