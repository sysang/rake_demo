import os

from flask import Flask
from flask import request
from flask import render_template

import yake

from rake_nltk import Rake

from keybert import KeyBERT


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/keywords_extraction')
    def hello():
        return render_template('index.html')

    @app.route('/yakeinput')
    def yake_input():

        return render_template('content_form.html', action='yakeoutput')

    @app.route('/yakeoutput', methods=['POST'])
    def yake_output():
        text = request.form['message']
        language = request.form['language']

        max_ngram_size = 3
        deduplication_thresold = 0.9
        deduplication_algo = 'seqm'
        windowSize = 1
        numOfKeywords = 20

        custom_kw_extractor = yake.KeywordExtractor(
                lan=language,
                n=max_ngram_size,
                dedupLim=deduplication_thresold,
                dedupFunc=deduplication_algo,
                windowsSize=windowSize,
                top=numOfKeywords,
                features=None)
        keywords = custom_kw_extractor.extract_keywords(text)

        return render_template('result.html', keywords=keywords, text=text, title='Yake Algorithm')

    @app.route('/rakeinput')
    def rake_input():

        return render_template('content_form.html', action='rakeoutput')

    @app.route('/rakeoutput', methods=['POST'])
    def rake_output():
        text = request.form['message']
        language = request.form['language']
        languages = {'en': 'english', 'dl': 'dutch'}

        r = Rake(language=languages[language], min_length=2, max_length=4)
        r.extract_keywords_from_text(text)
        keywords = r.get_ranked_phrases_with_scores()
        kws = []
        for kw in reversed(list(keywords)):
            kws.append((kw[1], kw[0]))

        return render_template('result.html', keywords=kws, text=text, title='Rake Algorithm')

    @app.route('/keybertinput')
    def keybert_input():

        return render_template('content_form.html', action='keybertoutput')

    @app.route('/keybertoutput', methods=['POST'])
    def keybert_output():
        text = request.form['message']

        model = KeyBERT('distilbert-base-nli-mean-tokens')
        keywords = model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words='english', use_maxsum=True, nr_candidates=20, top_n=10)

        return render_template('result.html', keywords=keywords, text=text, title='keyBERT algorithm')

    return app

