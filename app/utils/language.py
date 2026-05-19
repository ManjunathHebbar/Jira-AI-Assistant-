from langdetect import detect


def is_english(text):

    try:

        language = detect(text)

        return language == "en"

    except:

        return True