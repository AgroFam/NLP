from flask import Flask, request, jsonify
from translate import Translator
import langdetect
import requests
import json

app = Flask(__name__)

def translateText(text, language_codes):
    translations = {}
    for language, code in language_codes.items():
        try:
            # Detect the source language of the input text
            src_language = langdetect.detect(text)

            # Divide the text into chunks of 500 characters as it max translation length is 500 char only
            chunk_size = 500
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

            # Translate each chunk and store the translations in a list
            translated_chunks = []
            translator = Translator(to_lang=code, from_lang=src_language)
            for chunk in chunks:
                translation = translator.translate(chunk)
                translated_chunks.append(translation)

            # Concatenate the translations to form the final translation
            final_translation = ' '.join(translated_chunks)

            translations[language] = final_translation

        except (langdetect.lang_detect_exception.LangDetectException, StopIteration):
            translations[language] = 'Error: Could not detect language'

    return translations

@app.route("/translate", methods=["POST"])
def translate():
    text = request.form['text']

    # Load the language codes from the JSON file
    with open('languageCodes.json') as f:
        language_codes = json.load(f)

    # Translate the text to all the languages in the language codes file
    translations = translateText(text, language_codes)

    return jsonify({'translations': translations})

if __name__ == "__main__":
    app.run(debug=True)


#  "Urdu" : "ur",
#     "Assamese" : "as",
#     "Meitei" : "mni",
#     "Bodo" : "brx",
#     "Khasi" : "kha",
#     "Garo" : "grt",
#     "Kokborok" : "trp",
#     "Tripuri" : "tbw",
#     "Mizo" : "lus",
#     "Nagamese" : "nag",
#     "Manipuri" : "mni",
#     "Nepali" : "ne"