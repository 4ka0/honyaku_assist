from django.shortcuts import render
from django.conf import settings

from .forms import InputForm

from environs import Env
import deepl
from deepl.exceptions import DeepLException

from google.oauth2 import service_account
# from google.cloud import translate_v2 as translate  # For the basic API (v2)
from google.cloud import translate  # For the advanced API (v3)


def input_page_view(request):
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


def translation_direction(direction):
    if direction == "Ja>En":
        return "ja", "en"
    else:
        return "en", "ja"


def call_deepl_api(source_text, source_lang, target_lang):

    # Authenticate DeepL

    env = Env()
    env.read_env()
    try:
        translator = deepl.Translator(env.str("DEEPL_AUTH_KEY"))
    except DeepLException as e:
        result = "DeepL Error: " + str(e)
        usage = "Error"
        return result, usage

    # Get DeepL result

    # DeepL does not accept "en" as a target language code.
    # Has to be either "en-us" or "en-gb".
    if target_lang == "en":
        target_lang = "en-us"

    try:
        result = translator.translate_text(
                    source_text,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    glossary=None,
                )
    except DeepLException as e:
        result = "DeepL Error: " + str(e)
        usage = "Error"
        return result, usage

    # Get current DeepL usage

    try:
        usage = translator.get_usage()
    except DeepLException as e:
        result = f"{result}\n(DeepL Error: {str(e)}"
        usage = "Error"
        return result, usage

    return result, usage.character.count


def call_google_api_v3(source_text, source_lang, target_lang):
    """
    Method for calling the Google Translate API.
    Uses the Cloud Translation Advanced API (v3).
    """

    env = Env()
    env.read_env()

    # Authenticate

    service_account_key = str(settings.BASE_DIR.joinpath(env.str("GOOGLE_PROJECT_CREDENTIALS")))

    credentials = service_account.Credentials.from_service_account_file(
        service_account_key
    )

    # Translate

    try:
        client = translate.TranslationServiceClient(credentials=credentials)
    except Exception as e:
        return "Google Error: " + str(e)

    project_id = env.str("GOOGLE_PROJECT_ID")
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [source_text],
                "mime_type": "text/plain",  # mime types: text/plain, text/html
                "source_language_code": source_lang,
                "target_language_code": target_lang,
            }
        )
    except Exception as e:
        return "Google Error: " + str(e)

    if response.translations[0].translated_text:
        return response.translations[0].translated_text

    return "Error in translation response from Google."


'''
def call_google_api_v2(source_text, source_lang, target_lang):
    """
    Method for calling the Google Translate API.
    Uses the Cloud Translation Basic API (v2).
    """

    env = Env()
    env.read_env()

    google_service_account_key = str(settings.BASE_DIR.joinpath(env.str("GOOGLE_CREDENTIALS")))

    credentials = service_account.Credentials.from_service_account_file(
        google_service_account_key
    )

    translate_client = translate.Client(credentials=credentials)

    result = translate_client.translate(
        source_text,
        source_language=source_lang,
        target_language=target_lang,
    )

    return result["translatedText"]
'''
