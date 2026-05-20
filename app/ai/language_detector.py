from langdetect import detect
from langcodes import Language


def detect_language(text):

    try:

        language_code = detect(text)

        language_name = Language.get(
            language_code
        ).display_name()

        return language_name

    except Exception:

        return "Unknown"