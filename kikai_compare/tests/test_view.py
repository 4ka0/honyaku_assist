from django.urls import reverse
from django.test import SimpleTestCase

from deepl import translator


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
        self.valid_data_response = self.client.post(
            reverse('home'),
            {'direction': 'Ja>En', 'source_text': '花粉飛散情報',}
        )

    def test_output_page_status_code_with_valid_data(self):
        self.assertEqual(self.valid_data_response.status_code, 200)

    def test_output_page_basic_context_data_with_valid_data(self):
        self.assertEqual(self.valid_data_response.context['source_lang'], 'ja')
        self.assertEqual(self.valid_data_response.context['target_lang'], 'en-us')
        self.assertEqual(self.valid_data_response.context['source_text'], '花粉飛散情報')
        self.assertEqual(self.valid_data_response.context['source_text_length'], 6)

    def test_output_page_deepl_context_data_with_valid_data(self):
        self.assertIsInstance(
            self.valid_data_response.context['deepl_result'],
            translator.TextResult
        )
        self.assertIsInstance(self.valid_data_response.context['deepl_result_length'], int)
        self.assertGreater(self.valid_data_response.context['deepl_result_length'], 0)
        self.assertIsInstance(self.valid_data_response.context['deepl_usage'], int)
        self.assertGreater(self.valid_data_response.context['deepl_usage'], 0)

    def test_output_page_google_context_data_with_valid_data(self):
        self.assertIsInstance(self.valid_data_response.context['google_result'], str)
        self.assertGreater(len(self.valid_data_response.context['google_result']), 0)
        self.assertIsInstance(self.valid_data_response.context['google_result_length'], int)
        self.assertGreater(self.valid_data_response.context['google_result_length'], 0)

    def test_output_page_with_valid_data_status_code(self):
        self.assertEqual(self.valid_data_response.status_code, 200)

    def test_output_page_with_valid_data_templates_used(self):
        self.assertTemplateUsed(self.valid_data_response, 'base.html')
        self.assertTemplateUsed(self.valid_data_response, 'output.html')

    def test_output_page_with_valid_data_page_content(self):
        self.assertContains(self.valid_data_response, 'Source text (JA)')
        self.assertContains(self.valid_data_response, '(No. of characters: 6)')
        self.assertContains(self.valid_data_response, 'DeepL result (EN-US)')
        self.assertContains(self.valid_data_response, 'Google result (EN-US)')
        # Add tests to show mocked results from DeepL and Google are included in the output page
        # Tests are slow because each method is making real calls to the APIs

    def test_deep_api_exceptions(self):
        # Test exception is raised.
        # Test error message included in output.html.
        # Example, when en-us is set as the source language code:
        # (DeepL Error: Bad request, message: Value for 'source_lang' not supported.)
        pass
