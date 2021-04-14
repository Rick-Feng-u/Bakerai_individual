import os
from google.cloud import translate_v2 as translate

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\rickf\Github repo\Bakerai_individual\chatbot-310623-b5d2e50b3b60.json"

def languageDeteaction (input):
    translate_client = translate.Client()
    result = translate_client.detect_language(input)
    return result["language"]


def translateThis(input):
    translate_client = translate.Client()
    result = translate_client.translate(input, target_language='en')
    return result['translatedText']


def translateTo(text, target):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target)
    return result['translatedText']