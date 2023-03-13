from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

# Load the language codes from the JSON file
with open('languageCodes.json', 'r') as f:
    lang_codes = json.load(f)

@app.route('/translate-all', methods=['POST'])
def translate_all():
    # Get the text to translate from the request
    text = request.form['text']

    # Translate the text into all the languages
    translations = {}
    for lang, code in lang_codes.items():
        # Use the `trans` command to translate the text
        output = subprocess.check_output(['trans', '-b', code, ':', text], universal_newlines=True)
        translations[lang] = output.strip()

    # Return the translations as a JSON object
    return jsonify(translations)

if __name__ == '__main__':
    app.run()

