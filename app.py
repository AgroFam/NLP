from flask import Flask, request
import postTranslation
import IR

app = Flask(__name__)

app.add_url_rule('/azureTranslation', view_func=postTranslation.azure.translate_text)
app.add_url_rule('/multipleTranslation', view_func=postTranslation.multipleTranslation.translateText)
app.add_url_rule('/news', view_func=IR.news.google_search)
app.add_url_rule('/searchImage', view_func=IR.linkImage.retrieve_search_results)


if __name__ == '__main__':
   app.run()
