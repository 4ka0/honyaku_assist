from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import InputForm
from .utils import get_source_target_languages, call_deepl_api, call_google_api_v3


class IndexView(FormView):

    template_name = 'base.html'
    form_class = InputForm

    def form_valid(self, form):

        # Get form data
        translation_direction = form.cleaned_data["translation_direction"]
        source_text = form.cleaned_data["source_text"]
        source_text_length = len(source_text)

        # Determine source and target languages
        source_lang, target_lang = get_source_target_languages(translation_direction)

        # Get DeepL translation result
        deepl_result, deepl_usage = call_deepl_api(source_text, source_lang, target_lang)

        # Get Google translation result
        google_result, google_usage = call_google_api_v3(source_text, source_lang, target_lang)

        data = {
            "source_text": source_text,
            "source_text_length": source_text_length,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "deepl_result": deepl_result,
            "deepl_result_length": len(str(deepl_result)),
            "deepl_usage": deepl_usage,
            "google_result": google_result,
            "google_result_length": len(google_result),
            "google_usage": google_usage,
        }

        return render(self.request, "results.html", data)
