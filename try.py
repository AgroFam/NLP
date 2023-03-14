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



from googletrans import Translator
import argparse
import os

# init the translator
translator = Translator()

def translate(text, dest="en"):
    """Translate `text` to `dest`"""
    return translator.translate(text, dest=dest).text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Python script to translate text using Google Translate API (googletrans wrapper)")
    parser.add_argument("target", help="Text/Document to translate")
    parser.add_argument("-l", "--languages", help="Destination languages, comma-separated", required=True)
    parser.add_argument("-o", "--output", help="Output file name", required=True)
    
    args = parser.parse_args()
    target = args.target
    languages = args.languages.split(",")
    output_file = args.output
    
    if os.path.isfile(target):
        # translate a document instead
        # get basename of file
        basename = os.path.basename(target)
        # get the path dir
        dirname = os.path.dirname(target)
        try:
            filename, ext = basename.split(".")
        except:
            # no extension
            filename = basename
            ext = ""

        # read the text from the document
        text = open(target, encoding='utf-8').read()

        with open(output_file, "a", encoding='utf-8') as outfile:
            for lang in languages:
                # translate the text to the destination language
                translated_text = translate(text, dest=lang)

                # write to output file
                outfile.write(f"Translated text in {lang}:\n")
                outfile.write(translated_text)
                outfile.write("\n\n")
    else:
        # not a file, just text, print an error message
        print("Error: Input must be a file.")
