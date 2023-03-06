# For converting text into specified language mentioned by user

from flask import Flask, request, jsonify
from translate import Translator
import langdetect
import requests

app = Flask(__name__)

def translateText(text, dest_language):
    # Detect the source language of the input text
    src_language = langdetect.detect(text)
  
    # Divide the text into chunks of 500 characters as it max translation length is 500 char only
    chunk_size = 500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    # Translate each chunk and store the translations in a list
    translations = []
    translator = Translator(to_lang=dest_language, from_lang=src_language)
    for chunk in chunks:
        translation = translator.translate(chunk)
        translations.append(translation)

    # Concatenate the translations to form the final translation
    final_translation = ' '.join(translations)

    return final_translation

@app.route("/", methods=["GET"])
def hello():
    return jsonify({'status': "server is running... try hitting valid routes"})

@app.route("/translate", methods=["POST"])
def translate():
    text = request.form['text']
    dest_language = request.form['dest_language']
    translated_text = translateText(text, dest_language)
    #return translated_text
    return jsonify({'translation': translated_text})

if __name__ == "__main__":
    app.run(debug=True)
