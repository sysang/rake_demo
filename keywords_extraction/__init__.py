import os

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory

from . import algorithms


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

    @app.route('/favicon.ico')
    def serve_favicon():
        return send_from_directory('templates', 'favicon.ico')

    # a simple page that says hello
    @app.route('/')
    def hello():
        return render_template('index.html')

    @app.route('/yakeinput')
    def yake_input():

        return render_template('content_form.html', action='yakeoutput')

    @app.route('/yakeoutput', methods=['POST'])
    def yake_output():
        text = request.form['message']
        language = 'nl'

        keywords = algorithms.yake_impl(text, language)

        return render_template('result.html', keywords=keywords, text=text, title='Yake Algorithm')

    @app.route('/rakeinput')
    def rake_input():

        return render_template('content_form.html', action='rakeoutput')

    @app.route('/rakeoutput', methods=['POST'])
    def rake_output():
        text = request.form['message']
        language = 'nl'

        keywords = algorithms.rake_impl(text, language)

        return render_template('result.html', keywords=keywords, text=text, title='Rake Algorithm')

    @app.route('/keybertinput')
    def keybert_input():

        return render_template('content_form.html', action='keybertoutput')

    @app.route('/keybertoutput', methods=['POST'])
    def keybert_output():
        text = request.form['message']
        language = 'nl'

        keywords = algorithms.keybert_impl(text, language)

        return render_template('result.html', keywords=keywords, text=text, title='keyBERT algorithm')

    @app.route('/textrank', methods=['GET'])
    def textrank_input():

        return render_template('content_form.html', action='textrank')

    @app.route('/textrank', methods=['POST'])
    def textrank_output():
        text = request.form['message']
        language = 'nl'

        keywords = algorithms.textrank_impl(text, language)

        return render_template('result.html', keywords=keywords, text=text, title='TextRank algorithm')

    # Do not define route after the app return
    return app
