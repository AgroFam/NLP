# from googletrans import Translator
# import argparse
# import os

# # init the translator
# translator = Translator()

# def translate(text, dest="en"):
#     """Translate `text` to `dest`"""
#     return translator.translate(text, dest=dest).text

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Simple Python script to translate text using Google Translate API (googletrans wrapper)")
#     parser.add_argument("target", help="Text/Document to translate")
#     parser.add_argument("-l", "--languages", help="Destination languages, comma-separated", required=True)
    
#     args = parser.parse_args()
#     target = args.target
#     languages = args.languages.split(",")
    
#     if os.path.isfile(target):
#         # translate a document instead
#         # get basename of file
#         basename = os.path.basename(target)
#         # get the path dir
#         dirname = os.path.dirname(target)
#         try:
#             filename, ext = basename.split(".")
#         except:
#             # no extension
#             filename = basename
#             ext = ""

#         # read the text from the document
#         text = open(target, encoding='utf-8').read()

#         for lang in languages:
#             # translate the text to the destination language
#             translated_text = translate(text, dest=lang)

#             # write to new document file
#             new_filename = f"{filename}_{lang}.{ext}" if ext else f"{filename}_{lang}"
#             open(os.path.join(dirname, new_filename), "w", encoding='utf-8').write(translated_text)
#     else:
#         # not a file, just text, print an error message
#         print("Error: Input must be a file.")



# import argparse
# import os
# import googletrans
# from googletrans import Translator

# # init the translator
# translator = Translator()

# def translate(text, dest="en"):
#     """Translate `text` to `dest`"""
#     return translator.translate(text, dest=dest).text

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Simple Python script to translate text using Google Translate API (googletrans wrapper)")
#     parser.add_argument("target", help="Text/Document to translate")
#     parser.add_argument("-l", "--languages", help="Destination languages, comma-separated", required=True)
    
#     args = parser.parse_args()
#     target = args.target
#     languages = args.languages.split(",")
    
#     if os.path.isfile(target):
#         # translate a document instead
#         # get basename of file
#         basename = os.path.basename(target)
#         # get the path dir
#         dirname = os.path.dirname(target)
#         try:
#             filename, ext = basename.split(".")
#         except:
#             # no extension
#             filename = basename
#             ext = ""

#         # read the text from the document
#         text = open(target, encoding='utf-8').read()

#         for lang in languages:
#             # check if destination language is valid
#             if lang not in googletrans.LANGUAGES:
#                 print(f"Error: {lang} is not a valid language code.")
#                 continue
            
#             try:
#                 # translate the text to the destination language
#                 translated_text = translate(text, dest=lang)
#             except:
#                 print(f"Error: Failed to translate to {lang}.")
#                 continue

#             # write to new document file
#             new_filename = f"{filename}_{lang}.{ext}" if ext else f"{filename}_{lang}"
#             output_path = os.path.join(dirname, new_filename)
#             try:
#                 # ensure the output directory exists
#                 os.makedirs(os.path.dirname(output_path), exist_ok=True)
#                 open(output_path, "w", encoding='utf-8').write(translated_text)
#                 print(f"Translated to {lang}: {output_path}")
#             except:
#                 print(f"Error: Failed to write translated text to {output_path}.")
#     else:
#         # not a file, just text, print an error message
#         print("Error: Input must be a file.")



import argparse
import os
from google.cloud import translate_v2 as translate

# init the translator
translate_client = translate.Client()

def translate_text(text, target_language):
    """Translate `text` to `target_language`"""
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

def translate_file(input_path, output_dir, target_languages):
    """Translate a file at `input_path` to `target_languages` and save each output file in `output_dir`"""
    with open(input_path, 'r', encoding='utf-8') as f:
        input_text = f.read()
    filename, ext = os.path.splitext(os.path.basename(input_path))
    for target_language in target_languages:
        output_filename = f"{filename}_{target_language}{ext}"
        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            output_text = translate_text(input_text, target_language)
            f.write(output_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Python script to translate text or files to multiple languages using the Google Cloud Translation API")
    parser.add_argument("input", help="Text or file to translate")
    parser.add_argument("-o", "--output", help="Output directory for translated files. If not provided, outputs will be saved in the same directory as the input file.")
    parser.add_argument("-t", "--target-languages", help="Destination languages, comma-separated", required=True)

    args = parser.parse_args()
    input_path = args.input
    output_dir = args.output or os.path.dirname(input_path)
    target_languages = args.target_languages.split(",")

    if os.path.isfile(input_path):
        translate_file(input_path, output_dir, target_languages)
    else:
        input_text = input_path
        filename = 'translated'
        for target_language in target_languages:
            output_filename = f"{filename}_{target_language}.txt"
            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                output_text = translate_text(input_text, target_language)
                f.write(output_text)


