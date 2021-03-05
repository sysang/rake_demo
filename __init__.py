import os

from flask import Flask
from flask import request

import yake

from rake_nltk import Rake


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
    @app.route('/index')
    def hello():
        return '<ul>\
                <li>\
                    <a href="/yakeinput">Yake algorithm</a>\
                </li>\
                <li>\
                    <a href="/rakeinput">Rake (NLTK) algorithm</a>\
                </li>\
                </ul>'

    @app.route('/yakeinput')
    def yake_input():

        return '<form action="/yakeoutput" method="post">\
                    <textarea name="message" required style="width:450px; height:300px;" placeholder="Please enter content for execution..."></textarea><br><br>\
                    <input type="radio" checked id="lang1" name="language" value="en"><label for="lang1"> English</label><br> \
                    <input type="radio" id="lang2" name="language" value="dl"><label for="lang2"> Dutch</label><br><br><br> \
                    <input type="submit" value="SUBMIT">\
                </form'

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

        table = '<table><tr><th>Keywords</th><th>Score</th></tr>'
        for kw in keywords:
            table += '<tr><td>{}</td> <td>{}</td></tr>'.format(kw[0], kw[1])
        table += '</table>'

        res_body = '<div style="width:100%">\
                        <div style="width:40%; display:inline-block; vertical-align:top; padding: 15px">\
                            <h3 style="text-decoration: underline">\
                                <a target="_blank" href="https://github.com/LIAAD/yake">Yake Algorithm </a>\
                            </h3>\
                            <h4>Content</h4>\
                            <p>\
                                {}\
                            </p>\
                            <p><a href="/index" style="text-decoration: none"><< Index</a></p>\
                        </div>\
                        <div style="width:35%; display:inline-block; padding: 15px">\
                            {}\
                        </div>\
                    </div>'.format(text, table)

        return res_body

    @app.route('/rakeinput')
    def rake_input():

        return '<form action="/rakeoutput" method="post">\
                    <textarea name="message" required style="width:450px; height:300px;" placeholder="Please enter content for execution..."></textarea><br><br>\
                    <input type="radio" checked id="lang1" name="language" value="en"><label for="lang1"> English</label><br> \
                    <input type="radio" id="lang2" name="language" value="dl"><label for="lang2"> Dutch</label><br><br><br> \
                    <input type="submit" value="Submit">\
                </form'

    @app.route('/rakeoutput', methods=['POST'])
    def rake_output():
        text = request.form['message']
        language = request.form['language']
        languages = {'en': 'english', 'dl': 'dutch'}

        r = Rake(language=languages[language], min_length=2, max_length=4)
        r.extract_keywords_from_text(text)
        keywords = r.get_ranked_phrases_with_scores()

        table = '<table><tr><th>Keywords</th><th>Score</th></tr>'
        for kw in reversed(list(keywords)):
            table += '<tr><td>{}</td> <td>{}</td></tr>'.format(kw[1], kw[0])
        table += '</table>'

        res_body = '<div style="width:100%">\
                        <div style="width:40%; display:inline-block; vertical-align:top; padding: 15px">\
                            <h3 style="text-decoration: underline">\
                                <a target="_blank" href="https://github.com/csurfer/rake-nltk"> Rake (NTLK) Algorithm </a>\
                            </h3>\
                            <h4>Content</h4>\
                            <p>\
                                {}\
                            </p>\
                            <p><a href="/index" style="text-decoration: none"><< Index</a></p>\
                        </div>\
                        <div style="width:35%; display:inline-block; padding: 15px">\
                            {}\
                        </div>\
                    </div>'.format(text, table)

        return res_body

    return app
