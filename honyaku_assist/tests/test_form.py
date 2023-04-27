from django.test import TestCase
from django.forms.widgets import Textarea, RadioSelect

from ..forms import InputForm


class TestInputForm(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.empty_form = InputForm()
        cls.valid_form_ja_en = InputForm(
            {
                "translation_direction": "Ja>En",
                "source_text": "ゼルダの伝説シリーズは任天堂が開発しているコンピュータゲームシリーズ。",
            }
        )
        cls.valid_form_en_ja = InputForm(
            {
                "translation_direction": "En>Ja",
                "source_text": "Zelda series is a computer game series developed by Nintendo.",
            }
        )
        cls.invalid_form_no_direction = InputForm(
            {
                "translation_direction": "",
                "source_text": "Zelda series is a computer game series developed by Nintendo.",
            }
        )
        cls.invalid_form_no_source_text = InputForm(
            {
                "translation_direction": "Ja>En",
                "source_text": "",
            }
        )

    # Test field properties

    def test_direction_label(self):
        self.assertFalse(self.empty_form.fields["translation_direction"].label)
        self.assertNotEqual(self.empty_form.fields["translation_direction"].label, "")
        self.assertNotEqual(
            self.empty_form.fields["translation_direction"].label, "direction"
        )
        self.assertNotEqual(
            self.empty_form.fields["translation_direction"].label, "Direction"
        )

    def test_direction_widget(self):
        self.assertIsInstance(
            self.empty_form.fields["translation_direction"].widget, RadioSelect
        )

    def test_direction_choices(self):
        self.assertEqual(
            self.empty_form.fields["translation_direction"].choices,
            [
                ("Ja>En", "Japanese to English"),
                ("En>Ja", "English to Japanese"),
            ],
        )
        self.assertNotEqual(self.empty_form.fields["translation_direction"].choices, [])

    def test_direction_initial(self):
        self.assertEqual(
            self.empty_form.fields["translation_direction"].initial, "Ja>En"
        )
        self.assertNotEqual(
            self.empty_form.fields["translation_direction"].initial, "En>Ja"
        )
        self.assertNotEqual(self.empty_form.fields["translation_direction"].initial, "")

    def test_source_text_label(self):
        self.assertFalse(self.empty_form.fields["source_text"].label, None)
        self.assertNotEqual(self.empty_form.fields["source_text"].label, "")
        self.assertNotEqual(self.empty_form.fields["source_text"].label, "test_source")
        self.assertNotEqual(self.empty_form.fields["source_text"].label, "Test source")
        self.assertNotEqual(self.empty_form.fields["source_text"].label, "Test Source")

    def test_source_text_widget(self):
        self.assertIsInstance(self.empty_form.fields["source_text"].widget, Textarea)

    def test_source_text_max_length(self):
        self.assertEqual(self.empty_form.fields["source_text"].max_length, 1000)

    def test_source_text_strip(self):
        self.assertTrue(self.empty_form.fields["source_text"].strip)

    # Test submission of valid forms

    def test_valid_form_ja_en(self):
        self.assertTrue(self.valid_form_ja_en.is_bound)
        self.assertTrue(self.valid_form_ja_en.is_valid())
        self.assertEqual(len(self.valid_form_ja_en.errors), 0)
        self.assertEqual(self.valid_form_ja_en.errors, {})
        self.assertEqual(self.valid_form_ja_en.errors.as_text(), "")
        self.assertEqual(
            self.valid_form_ja_en.cleaned_data["translation_direction"], "Ja>En"
        )
        self.assertNotEqual(
            self.valid_form_ja_en.cleaned_data["translation_direction"], "En>Ja"
        )
        self.assertEqual(
            self.valid_form_ja_en.cleaned_data["source_text"],
            "ゼルダの伝説シリーズは任天堂が開発しているコンピュータゲームシリーズ。",
        )

    def test_valid_form_en_ja(self):
        self.assertTrue(self.valid_form_en_ja.is_bound)
        self.assertTrue(self.valid_form_en_ja.is_valid())
        self.assertEqual(len(self.valid_form_en_ja.errors), 0)
        self.assertEqual(self.valid_form_en_ja.errors, {})
        self.assertEqual(self.valid_form_en_ja.errors.as_text(), "")
        self.assertEqual(
            self.valid_form_en_ja.cleaned_data["translation_direction"], "En>Ja"
        )
        self.assertNotEqual(
            self.valid_form_en_ja.cleaned_data["translation_direction"], "Ja>En"
        )
        self.assertEqual(
            self.valid_form_en_ja.cleaned_data["source_text"],
            "Zelda series is a computer game series developed by Nintendo.",
        )

    # Test submission of invalid form: empty form

    def test_form_with_no_input(self):
        self.assertFalse(self.empty_form.is_bound)
        self.assertFalse(self.empty_form.is_valid())
        with self.assertRaises(AttributeError):
            self.empty_form.cleaned_data

    # Test submission of invalid form: invalid fields

    def test_invalid_form_no_direction(self):
        self.assertFalse(self.invalid_form_no_direction.is_valid())
        self.assertNotEqual(self.invalid_form_no_direction.errors, {})
        self.assertEqual(
            self.invalid_form_no_direction.errors["translation_direction"],
            ["This field is required."],
        )

    def test_invalid_form_no_source_text(self):
        self.assertFalse(self.invalid_form_no_source_text.is_valid())
        self.assertNotEqual(self.invalid_form_no_source_text.errors, {})
        self.assertEqual(
            self.invalid_form_no_source_text.errors["source_text"],
            ["This field is required."],
        )
