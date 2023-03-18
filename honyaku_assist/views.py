from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import InputForm
from .utils import translation_direction, call_deepl_api, call_google_api_v3


class IndexView(FormView):
    """
    A view for receiving source text to be translated via a form, and rendering
    translation results received from external APIs.
    Basically displays either:
    - a form to receive the source text to be translated from the user, or
    - the translation results received from the APIs.
    """

    template_name = 'base.html'
    form_class = InputForm

    def form_valid(self, form):

        # Get form data
        direction = form.cleaned_data["direction"]
        source_text = form.cleaned_data["source_text"]
        source_text_length = len(source_text)

        # Determine source and target languages
        source_lang, target_lang = translation_direction(direction)

        # Get translation results
        deepl_result, deepl_usage = call_deepl_api(source_text, source_lang, target_lang)
        deepl_result_length = len(str(deepl_result))
        google_result = call_google_api_v3(source_text, source_lang, target_lang)
        google_result_length = len(google_result)

        data = {
            "source_text": source_text,
            "source_text_length": source_text_length,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "deepl_result": deepl_result,
            "deepl_result_length": deepl_result_length,
            "deepl_usage": deepl_usage,
            "google_result": google_result,
            "google_result_length": google_result_length,
        }

        return render(self.request, "results.html", data)
