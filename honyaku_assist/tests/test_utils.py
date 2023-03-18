from unittest.mock import patch

from django.urls import reverse
from django.test import SimpleTestCase

import deepl


class TestOutput(SimpleTestCase):

    def setUp(self):

        # The below makes actual calls to the DeepL and Google APIs.
        """
        self.valid_data_response = self.client.post(
            reverse('index'),
            {'direction': 'Ja>En', 'source_text': '花粉飛散情報'}
        )
        """

        # The below mocks the calls to the DeepL and Google APIs.
        with patch('honyaku_assist.views.call_deepl_api') as mock_deepl_call, \
            patch('honyaku_assist.views.call_google_api_v3') as mock_google_call:

            # Mock the values returned by call_deepl_api() in the view.
            deepl_result, deepl_usage = 'Pollen dispersal information', 6
            mock_deepl_call.return_value = deepl_result, deepl_usage

            # Mock the values returned by call_google_api_v3() in the view.
            google_result = 'Pollen dispersion information'
            mock_google_call.return_value = google_result

            # Make a request to the view.
            self.response = self.client.post(
                reverse('index'),
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

    def test_output_page_templates_used(self):
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'output.html')

    def test_output_page_content(self):
        self.assertContains(self.response, 'Source text (JA)')
        self.assertContains(self.response, '(No. of characters: 6)')
        self.assertContains(self.response, 'DeepL result (EN-US)')
        self.assertContains(self.response, 'Pollen dispersal information')
        self.assertContains(self.response, 'Google result (EN-US)')
        self.assertContains(self.response, 'Pollen dispersion information')


class TestDeepLOutputErrors(SimpleTestCase):

    def test_deepl_api_exception_handling_1(self):

        with patch.object(deepl.Translator, 'translate_text') as mock_deepl_translator:

            # Mock the value returned by translate_text()
            mock_deepl_translator.return_value = 'A DeepL translation error occurred.'

            # Make a request to the view.
            response = self.client.post(
                reverse('index'),
                {'direction': 'Ja>En', 'source_text': '花粉飛散情報'}
            )

            # Assert that the mocked function is actually called.
            mock_deepl_translator.assert_called_once()

            self.assertEqual(response.status_code, 200)

            print(response.content)
            print(response.context)

    @patch('deepl.Translator')
    def test_deepl_api_exception_handling_1(self, mock_deepl_translator):
        mock_deepl_translator.translate_text.return_value = 'A DeepL translation error occurred.'
        mock_deepl_translator.get_usage.return_value = 10

        # Make a request to the view.
        response = self.client.post(
            reverse('index'),
            {'direction': 'Ja>En', 'source_text': '花粉飛散情報'}
        )

        mock_deepl_translator.assert_called_once()

        self.assertEqual(response.status_code, 200)

        # print(response.content)
        # print(response.context)
