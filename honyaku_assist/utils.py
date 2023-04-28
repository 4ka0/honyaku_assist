from django.conf import settings

from environs import Env
import deepl
from deepl.exceptions import DeepLException
from google.oauth2 import service_account
from google.cloud import translate  # For the advanced API (v3)
# from google.cloud import translate_v2 as translate  # For the basic API (v2)

from .models import Engine


def get_source_target_languages(translation_direction):
    """
    Method to determine the direction of the translation to be performed.
    DeepL accepts "en" as a source language code but not as a target language
    code (has to be either "en-us" or "en-gb"); "en-us" is set here.

    Args:
        translation_direction (str): The direction of translation.
            Either "Ja>En" of "En>Ja".

    Returns:
        Two strings representing the source language and the target language,
        respectively.
    """

    if translation_direction == "Ja>En":
        return "ja", "en-us"
    else:
        return "en", "ja"


def get_google_usage(source_text):
    """
    Method to return the usage for the Google translation engine.

    Args:
        source_text (str): The source text to be translated.

    Returns:
        current_usage (int): Number of characters translated in the
                             current month.
    """
    google_engine = Engine.objects.get(name="Google")
    google_engine.update_usage(source_text)
    return google_engine.current_usage


def call_deepl_api(source_text, source_lang, target_lang):
    """
    Calls the DeepL API to get a translation for source_text.

    Args:
        source_text (str): The source text to be translated.
        source_lang (str): The language of the source text.
        target_lang (str): The language to be translated into.

    Returns:
        result (str): The translation obtained from DeepL.
        usage (str): Number of characters translated in the current month.
    """

    env = Env()
    env.read_env()

    result, usage = "", ""

    try:
        # Authenticate with DeepL
        translator = deepl.Translator(env.str("DEEPL_AUTH_KEY"))

        # Get translation from DeepL
        result = translator.translate_text(
                source_text,
                source_lang=source_lang,
                target_lang=target_lang,
                glossary=None,
            )

        # Get current usage from DeepL
        usage_obj = translator.get_usage()
        usage = usage_obj.character.count

    except DeepLException as e:
        result = "DeepL error: " + str(e)
        return result, usage

    except Exception as e:
        result = "Error: " + str(e)
        return result, usage

    return result, usage


def call_google_api_v3(source_text, source_lang, target_lang):
    """
    Method for calling the Google Translate API.
    Uses the Cloud Translation Advanced API (v3).

    Args:
        source_text (str): The source text to be translated.
        source_lang (str): The language of the source text.
        target_lang (str): The language to be translated into.

    Returns:
        result (str): The translation obtained from Google.
        usage (int): Number of characters translated so far in the current month.
    """

    env = Env()
    env.read_env()

    try:
        # Authenticate

        service_account_key = str(settings.BASE_DIR.joinpath(env.str("GOOGLE_PROJECT_CREDENTIALS")))

        credentials = service_account.Credentials.from_service_account_file(
            service_account_key
        )

        client = translate.TranslationServiceClient(credentials=credentials)

        # Translate

        project_id = env.str("GOOGLE_PROJECT_ID")
        location = "global"
        parent = f"projects/{project_id}/locations/{location}"

        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [source_text],
                "mime_type": "text/plain",  # mime types: text/plain, text/html
                "source_language_code": source_lang,
                "target_language_code": target_lang,
            }
        )

        if response.translations[0].translated_text:
            result = response.translations[0].translated_text
        else:
            result = "Google error: Translation not included in response from Google."

    except Exception as e:
        result = "Google error: " + str(e)

    usage = get_google_usage(source_text)

    return result, usage


"""
def call_google_api_v2(source_text, source_lang, target_lang):

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
"""
