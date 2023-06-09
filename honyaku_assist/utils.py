import os
from django.conf import settings

# from environs import Env  # For local environment variables
import deepl
from deepl.exceptions import DeepLException
from google.oauth2 import service_account
from google.cloud import translate  # For the advanced API (v3)

# from google.cloud import translate_v2 as translate  # For the basic API (v2)

from .models import Engine


USAGE_LIMIT = 500000
USAGE_LIMIT_MESSAGE = (
    "Usage Error: Either this translation will result in this month's limit being exceeded, "
    "or this month's limit has already been exceeded. Please try again next month."
)


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


def get_google_usage():
    """
    Method to return the usage for the Google translation engine.

    Returns:
        current_usage (int): Number of characters translated in the
                             current month.
    """
    google_engine = Engine.objects.get(name="Google")
    return google_engine.current_usage


def update_google_usage(source_text):
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


def empty_check(result):
    """
    Method to check whether a translation result received from an API is empty.

    Args:
        result (str): The translation result from an API.

    Returns:
        output (str): Either the translation result unchanged,
                      or an error message.
    """
    if not result:
        return "API Error: No translation received."

    return result


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

    # For local environment variables
    # env = Env()
    # env.read_env()

    result, usage = "", ""

    try:
        # Authenticate
        # deepl_auth_key = env.str("DEEPL_AUTH_KEY")  # For local env variables
        deepl_auth_key = os.environ["DEEPL_AUTH_KEY"]  # For production env variables
        translator = deepl.Translator(deepl_auth_key)

        # Get current usage
        usage_obj = translator.get_usage()
        usage = usage_obj.character.count

        # Check current usage, and output error message if there is not enough
        # usage left to translate this source text.
        if usage + len(source_text) >= USAGE_LIMIT:
            result = USAGE_LIMIT_MESSAGE
        else:
            # Get translation
            result = translator.translate_text(
                source_text,
                source_lang=source_lang,
                target_lang=target_lang,
                glossary=None,
            )
            usage += len(source_text)

    except DeepLException as e:
        result = "DeepL Error: " + str(e)
        return result, usage

    except Exception as e:
        result = "Error: " + str(e)
        return result, usage

    result = empty_check(result)

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

    # For local environment variables
    # env = Env()
    # env.read_env()

    # Check current usage, and output error message if there is not enough
    # usage left to translate this source text.
    usage = get_google_usage()
    if usage + len(source_text) > USAGE_LIMIT:
        result = USAGE_LIMIT_MESSAGE
    else:
        # Get translation from Google
        try:
            # Authenticate
            service_account_key = str(
                # settings.BASE_DIR.joinpath(env.str("GOOGLE_PROJECT_CREDENTIALS"))  # Local
                settings.BASE_DIR.joinpath(os.environ["GOOGLE_PROJECT_CREDENTIALS"])  # Production
            )
            credentials = service_account.Credentials.from_service_account_file(
                service_account_key
            )
            client = translate.TranslationServiceClient(credentials=credentials)

            # Set up Google project params
            # project_id = env.str("GOOGLE_PROJECT_ID")  # Local version
            project_id = os.environ["GOOGLE_PROJECT_ID"]  # Deployment version

            location = "global"
            parent = f"projects/{project_id}/locations/{location}"

            # Get translation
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
                result = (
                    "Error: Translation not included in response from Google."
                )

        except Exception as e:
            result = "Google Error: " + str(e)

        usage = update_google_usage(source_text)
        result = empty_check(result)

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
