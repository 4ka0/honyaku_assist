from django.test import TestCase
from django.forms.widgets import Textarea, RadioSelect

from .forms import InputForm


class TestInputForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.empty_form = InputForm()

    # Test field properties

    def test_direction_label(self):
        self.assertEqual(self.empty_form.fields["direction"].label, None)
        self.assertNotEqual(self.empty_form.fields["direction"].label, "")
        self.assertNotEqual(self.empty_form.fields["direction"].label, "direction")
        self.assertNotEqual(self.empty_form.fields["direction"].label, "Direction")

    def test_direction_widget(self):
        self.assertIsInstance(self.empty_form.fields['direction'].widget, RadioSelect)

    def test_direction_choices(self):
        self.assertEqual(
            self.empty_form.fields['direction'].choices,
            [
                ("Ja>En", "Japanese to English"),
                ("En>Ja", "English to Japanese"),
            ],
        )
        self.assertNotEqual(self.empty_form.fields['direction'].choices, [])

    def test_direction_initial(self):
        self.assertEqual(self.empty_form.fields['direction'].initial, "Ja>En")
        self.assertNotEqual(self.empty_form.fields['direction'].initial, "En>Ja")
        self.assertNotEqual(self.empty_form.fields['direction'].initial, "")

    def test_source_text_label(self):
        self.assertEqual(self.empty_form.fields["source_text"].label, None)
        self.assertNotEqual(self.empty_form.fields["source_text"].label, "")
        self.assertNotEqual(self.empty_form.fields["source_text"].label, "test_source")
        self.assertNotEqual(self.empty_form.fields["source_text"].label, "Test source")
        self.assertNotEqual(self.empty_form.fields["source_text"].label, "Test Source")

    def test_source_text_widget(self):
        self.assertIsInstance(self.empty_form.fields['source_text'].widget, Textarea)

    def test_source_text_max_length(self):
        self.assertEqual(self.empty_form.fields['source_text'].max_length, 1000)

    def test_source_text_strip(self):
        self.assertTrue(self.empty_form.fields['source_text'].strip)

    # Test submission of valid form
    # Test submission of invalid form: empty form
    # Test submission of invalid form: invalid fields
