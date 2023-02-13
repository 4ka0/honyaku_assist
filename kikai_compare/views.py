from django.shortcuts import render

from .forms import InputForm

from environs import Env
import deepl


def input_page_view(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():

            # Get form data
            direction = form.cleaned_data["direction"]
            source_text = form.cleaned_data["source_text"]

            # Determine source and target languages
            source_lang, target_lang = translation_direction(direction)

            # Get translation results
            deepl_result = call_deepl_api(source_text, source_lang, target_lang)

            return render(
                request,
                "output.html",
                {
                    "source_text": source_text,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "deepl_result": deepl_result,
                },
            )
    else:
        form = InputForm()
    return render(request, 'input.html', {'form': form})


def output_page_view(request):
    return render(request, 'output.html')


def translation_direction(direction):
    if direction == "Ja>En":
        return "ja", "en-us"
    else:
        return "en-us", "ja"


def call_deepl_api(source_text, source_lang, target_lang):
    env = Env()
    env.read_env()
    auth_key = env.str("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    deepl_result = translator.translate_text(
                source_text,
                source_lang=source_lang,
                target_lang=target_lang,
                glossary=None,
            )
    return deepl_result
