from django.urls import reverse
from django.test import SimpleTestCase

from deepl import translator


class TestInputPageView(SimpleTestCase):

    def test_input_page_exists_at_desired_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_input_page_accessible_by_name(self):
        response = self.client.get(reverse('input'))
        self.assertEqual(response.status_code, 200)

    def test_input_page_uses_correct_template(self):
        response = self.client.get(reverse('input'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'input.html')

    def test_input_page_title_and_navbar_content(self):
        response = self.client.get(reverse('input'))
        self.assertContains(response, '<title>Honyaku Assist</title>')

    def test_input_page_navbar_content(self):
        response = self.client.get(reverse('input'))
        self.assertContains(response, '<a class="navbar-brand" href="/">Honyaku Assist</a>')
        self.assertContains(response, '<span class="navbar-text">A machine translation assistant for')

    def test_input_page_form_content(self):
        response = self.client.get(reverse('input'))
        self.assertContains(response, 'Japanese to English')
        self.assertContains(response, 'English to Japanese')
        self.assertContains(response, 'Translate</button>')

    def test_output_page_context(self):
        response = self.client.post(
            reverse('input'),
            {'direction': 'Ja>En', 'source_text': '花粉飛散情報',}
        )

        self.assertEqual(response.context['source_lang'], 'ja')
        self.assertEqual(response.context['target_lang'], 'en-us')
        self.assertEqual(response.context['source_text'], '花粉飛散情報')
        self.assertEqual(response.context['source_text_length'], 6)

        self.assertIsInstance(response.context['deepl_result'], translator.TextResult)
        self.assertIsInstance(response.context['deepl_result_length'], int)
        self.assertGreater(response.context['deepl_result_length'], 0)
        self.assertIsInstance(response.context['deepl_usage'], int)
        self.assertGreater(response.context['deepl_usage'], 0)

        self.assertIsInstance(response.context['google_result'], str)
        self.assertGreater(len(response.context['google_result']), 0)
        self.assertIsInstance(response.context['google_result_length'], int)
        self.assertGreater(response.context['google_result_length'], 0)

    def test_output_page_content(self):
        response = self.client.post(
            reverse('input'),
            {'direction': 'Ja>En', 'source_text': '花粉飛散情報',}
        )

        # print('\n**********')
        # print(response)
        # print('**********')
        # print(response.content)
        # print('**********')
        # print(response.context)
        # print('**********')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Source text (JA)')
        self.assertContains(response, 'DeepL result (EN-US)')
        self.assertContains(response, 'Google result (EN-US)')
