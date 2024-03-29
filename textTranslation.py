from translate import Translator
import langdetect

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

# Get the text and language codes from the user
text = input("Enter the text to be translated: ")
dest_language = input("Enter the target language code (e.g. hi for Hindi): ")

# Translate the text
translatedText = translateText(text, dest_language)

# Print the final translation
print(f"Translation: {translatedText}")
