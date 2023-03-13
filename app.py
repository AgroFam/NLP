import os
from flask import Flask, request
from postTranslation.azure import translate_text
from postTranslation.multipleTranslation import multipleTranslation
from IR.news import google_search
from IR.linkImage import retrieve_search_results
import hello

app = Flask(__name__)

app.add_url_rule('/azureTranslation', view_func=translate_text)
app.add_url_rule('/multipleTranslation', view_func=multipleTranslation)
app.add_url_rule('/news', view_func=google_search)
app.add_url_rule('/searchImage', view_func=retrieve_search_results)
app.add_url_rule('/', view_func=hello.hello)

if __name__ == '__main__':
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)