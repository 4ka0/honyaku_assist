from django.urls import reverse
from django.test import SimpleTestCase


class TestIndexPage(SimpleTestCase):

    def test_index_page_exists_at_desired_url(self):
        response = self.client.get("")

        self.assertEqual(response.status_code, 200)

    def test_index_page_accessible_by_name(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)

    def test_index_page_uses_correct_template(self):
        response = self.client.get(reverse("index"))

        self.assertTemplateUsed(response, "base.html")

    def test_index_page_title_and_navbar_content(self):
        response = self.client.get(reverse("index"))

        self.assertContains(response, "<title>Honyaku Assist</title>")

    def test_index_page_navbar_content(self):
        response = self.client.get(reverse("index"))

        self.assertContains(
            response, '<a class="navbar-brand" href="/">Honyaku Assist</a>'
        )
        self.assertContains(
            response, '<span class="navbar-text">A machine translation assistant for'
        )

    def test_index_page_form_content(self):
        response = self.client.get(reverse("index"))

        self.assertContains(response, "Japanese to English")  # Radio button label
        self.assertContains(response, "English to Japanese")  # Radio button label
        self.assertContains(response, "Translate")  # Submit button text

    def test_textarea_is_required_and_has_autofocus(self):
        response = self.client.get(reverse("index"))
        expected = (
            '<textarea name="source_text" cols="40" rows="8" autofocus '
            'maxlength="1000" class="textarea form-control" required id="id_source_text">'
        )

        self.assertContains(response, expected)

    def test_japanese_to_english_radio_button_is_required_and_is_checked(self):
        response = self.client.get(reverse("index"))
        expected = (
            '<input type="radio" class="form-check-input"  name="translation_direction" '
            'value="Ja&gt;En"  id="id_translation_direction_0" required checked>'
        )

        self.assertContains(response, expected)

    def test_english_to_japanese_radio_button_is_required(self):
        response = self.client.get(reverse("index"))
        expected = (
            '<input type="radio" class="form-check-input"  name="translation_direction" '
            'value="En&gt;Ja"  id="id_translation_direction_1" required>'
        )
        
        self.assertContains(response, expected)
