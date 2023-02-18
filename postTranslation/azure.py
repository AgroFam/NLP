from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Set up the endpoint and subscription key for the Microsoft Translator API
translate_endpoint = "https://api.cognitive.microsofttranslator.com/translate"
translate_subscription_key = "YOUR_SUBSCRIPTION_KEY"

def translate_text(text, dest_language):
    # Set up the translation parameters
    params = {
        "api-version": "3.0",
        "from": "",
        "to": dest_language
    }
    
    # Detect the source language of the input text
    detect_endpoint = "https://api.cognitive.microsofttranslator.com/detect"
    detect_headers = {
        "Ocp-Apim-Subscription-Key": translate_subscription_key,
        "Content-Type": "application/json"
    }
    detect_payload = [{
        "text": text
    }]
    detect_response = requests.post(detect_endpoint, headers=detect_headers, json=detect_payload)
    detect_response.raise_for_status()
    src_language = detect_response.json()[0]["language"]
    
    # Divide the text into chunks of 5000 characters as it max translation length is 5000 char only
    chunk_size = 5000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    # Translate each chunk and store the translations in a list
    translations = []
    for chunk in chunks:
        translate_headers = {
            "Ocp-Apim-Subscription-Key": translate_subscription_key,
            "Content-Type": "application/json"
        }
        params["from"] = src_language
        translate_payload = [{
            "text": chunk
        }]
        translate_response = requests.post(translate_endpoint, headers=translate_headers, params=params, json=translate_payload)
        translate_response.raise_for_status()
        translation = translate_response.json()[0]["translations"][0]["text"]
        translations.append(translation)

    # Concatenate the translations to form the final translation
    final_translation = ' '.join(translations)

    return final_translation

@app.route("/translate", methods=["POST"])
def translate():
    text = request.form['text']
    dest_language = request.form['dest_language']
    translated_text = translate_text(text, dest_language)
    return jsonify({'translation': translated_text})

if __name__ == "__main__":
    app.run(debug=True)
