import re
import string


def check_lang(translator, text):
    """
    Check the language of an input string.

    Parameters
    ----------
    translator : googletrans.client.Translator
        Translator from the googletrans package to check the text language.
    text : str
        An input string which language is checked.

    Returns
    -------
    str
        Short form of the detected language of the text, e.g. 'en' or 'de'.
    """
    if len(text) > 5000:
        text = text[:4999]
    return translator.detect(text).lang


def translate(translator, text):
    """
    Translate an input string into the english language.

    Parameters
    ----------
    translator : translate package
        Translator from https://pypi.org/project/translate/.
    text : str
        An input string which should be translated.

    Returns
    -------
    text : str
        Translated input string. The output text's language is english.
    """
    if len(text) > 5000:
        text_ = translator.translate(text[:4999], dest='en').text
        for word in text[4999:].split():
            if len(word) > 0:
                text_ += translator.translate(word, dest='en').text + ' '
        text = text_
    else:
        text = translator.translate(text, dest='en')
    print(text)
    return text


def clean_lyrics(astr):
    """
    Remove numbers, punctuation and non-alphabetic characters from an input str.
    Puts the input string in lower letters.

    Parameters
    ----------
    astr : str
        The input string.

    Returns
    -------
    nonpunct : str
        Cleaned input string.
    """
    if "ContributorsTranslationsTürkçeEspañolPortuguês日本語ItalianoΕλληνικάDeutschFrançaisEnglishEnglishNederlandsShqipPolski한국어" in astr:
        astr = astr.split("ContributorsTranslationsTürkçeEspañolPortuguês日本語ItalianoΕλληνικάDeutschFrançaisEnglishEnglishNederlandsShqipPolski한국어")[1]
    astr = re.sub(r"[^\x00-\x7F]+", " ", astr)
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')  # remove punctuation and numbers
    nopunct = regex.sub(" ", astr.lower())
    return nopunct
