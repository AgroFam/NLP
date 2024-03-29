# from flask import Flask, jsonify, request
# from googletrans import LANGUAGES, Translator
# import re

# app = Flask(__name__)
# translator = Translator()

# # Translate text to one or more languages
# def translate(text, dest_languages):
#     translations = {}
#     for lang_code, lang_name in LANGUAGES.items():
#         if lang_code in dest_languages:
#             # Translate text to the target language
#             translated_text = translator.translate(text, dest=lang_code).text
          
#             translations[lang_name] = translated_text
#     return translations

# # Flask route to translate text
# @app.route('/translate', methods=['POST'])
# def translate_text():
#     data = request.json
#     text = data['text']
#     dest_languages = data['dest_languages'].split(',')
#     translations = translate(text, dest_languages)
#     return jsonify(translations)

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, jsonify, request
from googletrans import LANGUAGES, Translator
import re

app = Flask(__name__)
translator = Translator()

    # Translate text to one or more languages
def translate(text, dest_languages):
    # Replace double quotes with single quotes
    text = text.replace('"', "'")
    print(text)

    translations = {}
    for lang_code, lang_name in LANGUAGES.items():
        if lang_code in dest_languages:
            # Translate text to the target language
            translated_text = translator.translate(text, dest=lang_code).text
        
            translations[lang_name] = translated_text
    return translations



# Flask route to translate text
# @app.route('/translate', methods=['POST'])
# def translate_text():
#     data = request.json
#     text = data['text']
#     dest_languages = data['dest_languages'].split(',')
#     translations = translate(text, dest_languages)
#     return jsonify(translations)

# Flask route to translate text
@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.json
        if data is None:
            return jsonify({'error': 'Invalid JSON data in the request'}), 400

        if 'text' in data:
            text = data['text']
        else:
            return jsonify({'error': 'Missing text parameter'}), 400

        if 'dest_languages' in data:
            dest_languages = data['dest_languages'].split(',')
        else:
            return jsonify({'error': 'Missing dest_languages parameter'}), 400

        translations = translate(text, dest_languages)
        return jsonify(translations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)