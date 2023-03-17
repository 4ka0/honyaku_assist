from django.shortcuts import render

from .forms import InputForm
from .utils import translation_direction, call_deepl_api, call_google_api_v3


def translate_view(request):
    """
    View for the homepage. Basically displays either:
    (1) a form to receive the source text to be translated from the user, or
    (2) the translation results received from the DeepL and Google APIs.
    """

    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():

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

            return render(
                request,
                "output.html",
                {
                    "source_text": source_text,
                    "source_text_length": source_text_length,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "deepl_result": deepl_result,
                    "deepl_result_length": deepl_result_length,
                    "deepl_usage": deepl_usage,
                    "google_result": google_result,
                    "google_result_length": google_result_length,
                },
            )
    else:
        form = InputForm()
    return render(request, 'input.html', {'form': form})
