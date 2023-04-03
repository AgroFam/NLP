import os
from flask import Flask, request
from flask_cors import CORS
from postTranslation.azure import translate_text
from postTranslation.translate import translate_text
from IR.news import google_search
from IR.linkImage import get_news
import hello
from waitress import serve

app = Flask(__name__)
CORS(app)
print('Starting server...')

app.add_url_rule('/azureTranslation', view_func=translate_text)
app.add_url_rule('/translate', view_func=translate_text)
app.add_url_rule('/searchImage', view_func=google_search)
app.add_url_rule('/news', view_func=get_news)
app.add_url_rule('/', view_func=hello.hello)

if __name__ == '__main__':
   port = int(os.environ.get('PORT', 5000))
   serve(app, host='0.0.0.0', port=port)
   # app.run()

